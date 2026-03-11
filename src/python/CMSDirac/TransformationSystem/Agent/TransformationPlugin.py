from __future__ import annotations

from typing import Any

from DIRAC import S_ERROR, S_OK
from DIRAC.TransformationSystem.Client.TransformationClient import TransformationClient
from DIRAC.TransformationSystem.Agent.TransformationPlugin import (
    TransformationPlugin as DIRACTransformationPlugin,
)


class TransformationPlugin(DIRACTransformationPlugin):
    """
    CMS extension of DIRAC's TransformationPlugin.

    Stage-1 scope:
      - consume normalized plugin parameters produced by bin/wmc2transf.py
      - support the example workflow shape
      - implement EventBased splitting first
      - keep the code testable with simple in-memory records

    Expected params from the translator:
      {
        "Mode": "EventBased",
        "EventsPerJob": 100,
        "FilesPerJob": null,
        "LumisPerJob": null,
        "EventsPerLumi": 100,
        "StaticDatasetMode": true,
        "ResourceHints": {...}
      }

    Supported self.data shapes:
      1) DIRAC-like dict keyed by LFN:
         {
           "/store/..../file1.root": {"SEs": ["SE_1"], "Events": 100},
           ...
         }

      2) simplified test records:
         {
           "/store/..../file1.root": {"se": "SE_1", "events": 100},
           ...
         }

      3) list of dicts, for unit-like testing:
         [
           {"lfn": "/store/.../file1.root", "se": "SE_1", "events": 100},
           ...
         ]


    Example usage:

        In [7]: plugin = TransformationPlugin("CMSWMCoreSplittingPlugin")
        In [8]: plugin.params = {
                   "Mode": "EventBased",
                   "EventsPerJob": 100,
                   "StaticDatasetMode": True}

        In [9]: plugin.setInputData(
                {
                    "/store/test/file1.root": {"se": "T2_TEST_SE", "events": 100},
                    "/store/test/file2.root": {"se": "T2_TEST_SE", "events": 100},
                    "/store/test/file3.root": {"se": "T2_TEST_SE", "events": 100},
                }
            )

    Expected result:
        In [10]: result = plugin._CMSWMCoreSplittingPlugin()

        In [11]: %page result
        {'OK': True,
         'Value': [('T2_TEST_SE', ['/store/test/file1.root']),
                   ('T2_TEST_SE', ['/store/test/file2.root']),
                   ('T2_TEST_SE', ['/store/test/file3.root'])]}

    Change Events per job:
        In [22]: plugin.params = {
                     "Mode": "EventBased",
                     "EventsPerJob": 250,
                     "StaticDatasetMode": True
                 }
        In [23]: result = plugin._CMSWMCoreSplittingPlugin()

    Expected result:
        In [24]: %page result
        {'OK': True,
         'Value': [('T2_TEST_SE', ['/store/test/file1.root', '/store/test/file2.root']),
                   ('T2_TEST_SE', ['/store/test/file3.root'])]}
    """

    def __init__(self, plugin: str, transClient=None):
        super().__init__(plugin)
        if transClient is None:
            self.transClient = TransformationClient()
        else:
            self.transClient = transClient

    # -------------------------------------------------------------------------
    # Public plugin entry points
    # -------------------------------------------------------------------------

    def _CMSWMCoreSplittingPlugin(self):
        """
        Main plugin entry point.

        Dispatches to the normalized splitting mode declared in self.params["Mode"].
        """
        if not self.isOK():
            return S_ERROR("CMSWMCoreSplittingPlugin: missing self.data or self.params")

        mode = self.params.get("Mode", "EventBased")

        if mode == "EventBased":
            return self._run_event_based()

        if mode == "FileBased":
            return self._run_file_based()

        if mode == "LumiBased":
            return self._run_lumi_based()

        if mode == "EventAwareLumiBased":
            return self._run_event_aware_lumi_based()

        return S_ERROR(f"CMSWMCoreSplittingPlugin: unsupported Mode='{mode}'")

    # Optional aliases, useful if you later decide to map directly to them.
    def _ByEvent(self):
        return self._run_event_based()

    def _ByFile(self):
        return self._run_file_based()

    def _ByLumi(self):
        return self._run_lumi_based()

    def _ByEventAwareLumi(self):
        return self._run_event_aware_lumi_based()

    # -------------------------------------------------------------------------
    # Normalization helpers
    # -------------------------------------------------------------------------

    def _iter_records(self) -> list[dict[str, Any]]:
        """
        Normalize self.data into:
          [
            {
              "lfn": str,
              "se": str,
              "events": int | None,
              "lumis": int | None,
              "runs": list[int],
              "raw": {...}
            },
            ...
          ]
        """
        records = []

        if isinstance(self.data, list):
            for entry in self.data:
                if not isinstance(entry, dict):
                    continue
                lfn = entry.get("lfn")
                if not lfn:
                    continue
                records.append(
                    {
                        "lfn": lfn,
                        "se": entry.get("se") or entry.get("SE") or "UnknownSE",
                        "events": self._safe_int(
                            entry.get("events", entry.get("Events"))
                        ),
                        "lumis": self._safe_int(
                            entry.get("lumis", entry.get("Lumis"))
                        ),
                        "runs": entry.get("runs", entry.get("Runs", [])) or [],
                        "raw": entry,
                    }
                )
            return records

        if isinstance(self.data, dict):
            for lfn, meta in self.data.items():
                if not isinstance(meta, dict):
                    meta = {}

                se = (
                    meta.get("se")
                    or meta.get("SE")
                    or self._extract_first_se(meta)
                    or "UnknownSE"
                )

                records.append(
                    {
                        "lfn": lfn,
                        "se": se,
                        "events": self._safe_int(
                            meta.get("events", meta.get("Events"))
                        ),
                        "lumis": self._safe_int(
                            meta.get("lumis", meta.get("Lumis"))
                        ),
                        "runs": meta.get("runs", meta.get("Runs", [])) or [],
                        "raw": meta,
                    }
                )
            return records

        return []

    @staticmethod
    def _safe_int(value):
        if value in (None, "", False):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _extract_first_se(meta: dict[str, Any]) -> str | None:
        """
        Best-effort extraction of an SE from common metadata shapes.
        """
        for key in ("SEs", "Replicas", "ReplicaSEs"):
            value = meta.get(key)
            if isinstance(value, list) and value:
                return str(value[0])
            if isinstance(value, tuple) and value:
                return str(value[0])
            if isinstance(value, dict) and value:
                return str(next(iter(value.keys())))
        return None

    def _group_records_by_se(self, records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        grouped = {}
        for record in records:
            grouped.setdefault(record["se"], []).append(record)
        return grouped

    # -------------------------------------------------------------------------
    # Splitting implementations
    # -------------------------------------------------------------------------

    def _run_event_based(self):
        """
        Group LFNs so that the total event count per task does not exceed EventsPerJob.

        This is the primary mode needed for the current example workflow.
        """
        events_per_job = self._safe_int(self.params.get("EventsPerJob"))
        if not events_per_job or events_per_job <= 0:
            return S_ERROR(
                "CMSWMCoreSplittingPlugin(EventBased): EventsPerJob must be a positive integer"
            )

        records = self._iter_records()
        if not records:
            return S_ERROR("CMSWMCoreSplittingPlugin(EventBased): no input records")

        tasks = []
        by_se = self._group_records_by_se(records)

        for se, se_records in by_se.items():
            current_lfns = []
            current_events = 0

            for record in se_records:
                events = record["events"]

                # Fallback for records without event metadata:
                # treat them as one whole-file work unit.
                if events is None:
                    events = events_per_job

                if current_lfns and (current_events + events > events_per_job):
                    tasks.append((se, current_lfns))
                    current_lfns = []
                    current_events = 0

                current_lfns.append(record["lfn"])
                current_events += events

            if current_lfns:
                tasks.append((se, current_lfns))

        return S_OK(tasks)

    def _run_file_based(self):
        """
        Group LFNs by FilesPerJob.
        """
        files_per_job = self._safe_int(self.params.get("FilesPerJob"))
        if not files_per_job or files_per_job <= 0:
            return S_ERROR(
                "CMSWMCoreSplittingPlugin(FileBased): FilesPerJob must be a positive integer"
            )

        records = self._iter_records()
        if not records:
            return S_ERROR("CMSWMCoreSplittingPlugin(FileBased): no input records")

        tasks = []
        by_se = self._group_records_by_se(records)

        for se, se_records in by_se.items():
            chunk = []
            for record in se_records:
                chunk.append(record["lfn"])
                if len(chunk) >= files_per_job:
                    tasks.append((se, chunk))
                    chunk = []
            if chunk:
                tasks.append((se, chunk))

        return S_OK(tasks)

    def _run_lumi_based(self):
        """
        Minimal placeholder lumi grouping.

        Stage-1 limitation:
        if lumi counts are absent, fall back to one-file-per-task.
        """
        lumis_per_job = self._safe_int(self.params.get("LumisPerJob"))
        if not lumis_per_job or lumis_per_job <= 0:
            return S_ERROR(
                "CMSWMCoreSplittingPlugin(LumiBased): LumisPerJob must be a positive integer"
            )

        records = self._iter_records()
        if not records:
            return S_ERROR("CMSWMCoreSplittingPlugin(LumiBased): no input records")

        tasks = []
        by_se = self._group_records_by_se(records)

        for se, se_records in by_se.items():
            current_lfns = []
            current_lumis = 0

            for record in se_records:
                lumis = record["lumis"]
                if lumis is None:
                    lumis = lumis_per_job

                if current_lfns and (current_lumis + lumis > lumis_per_job):
                    tasks.append((se, current_lfns))
                    current_lfns = []
                    current_lumis = 0

                current_lfns.append(record["lfn"])
                current_lumis += lumis

            if current_lfns:
                tasks.append((se, current_lfns))

        return S_OK(tasks)

    def _run_event_aware_lumi_based(self):
        """
        Minimal combined policy:
          - prefer EventsPerJob if available
          - otherwise fall back to LumisPerJob
          - do not split files internally yet

        This is intentionally conservative for stage 1.
        """
        if self._safe_int(self.params.get("EventsPerJob")):
            return self._run_event_based()

        if self._safe_int(self.params.get("LumisPerJob")):
            return self._run_lumi_based()

        return S_ERROR(
            "CMSWMCoreSplittingPlugin(EventAwareLumiBased): requires EventsPerJob or LumisPerJob"
        )
