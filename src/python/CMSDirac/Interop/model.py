from dataclasses import dataclass, field
from typing import Any


@dataclass
class CanonicalStep:
    StepName: str
    Executable: str
    Arguments: list[str]
    SoftwareVersion: str | None = None
    SoftwareArchitecture: str | None = None
    MemoryMB: int | None = None
    CpuCores: int | None = None
    CpuTime: int | None = None
    GpuRequired: bool = False
    InputArtifacts: list[str] = field(default_factory=list)
    OutputArtifacts: list[str] = field(default_factory=list)
    Environment: dict[str, str] = field(default_factory=dict)
    SourceRef: dict[str, str] = field(default_factory=dict)


@dataclass
class CanonicalSplitting:
    PluginName: str
    SplitMode: str
    FilesPerJob: int | None = None
    EventsPerJob: int | None = None
    LumisPerJob: int | None = None
    EventsPerLumi: int | None = None
    ResourceHints: dict[str, Any] = field(default_factory=dict)
    StaticDatasetMode: bool = True
    SourceRef: dict[str, str] = field(default_factory=dict)


@dataclass
class CanonicalTask:
    TaskName: str
    TaskPath: str
    ParentTaskNames: list[str]
    TransformationType: str
    TransformationGroup: str
    TransformationFamily: str
    Priority: int | None
    InputDataset: dict[str, Any]
    OutputDataset: dict[str, Any]
    SitePolicy: dict[str, Any]
    Step: CanonicalStep
    Splitting: CanonicalSplitting
    SourceRef: dict[str, str] = field(default_factory=dict)


@dataclass
class CanonicalProduction:
    ProductionName: str
    ProductionType: str
    Priority: int | None = None


@dataclass
class TranslationDocument:
    SchemaVersion: str
    SourceSystem: str
    TargetSystem: str
    Production: CanonicalProduction
    Tasks: list[CanonicalTask]
