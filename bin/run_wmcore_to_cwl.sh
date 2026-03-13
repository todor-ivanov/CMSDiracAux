#!/usr/bin/env bash

# End-to-end runner for the WMCore → DIRAC → CWL PoC pipeline

set -euo pipefail


# ------------------------------------------------------------
# Parameters
# ------------------------------------------------------------

REQUEST_NAME="${1:-pdmvserv_RVCMSSW_16_0_0_pre2QCD__STD_GPU_Pix_202_PU_KIT_251125_103426_8717}"

CMS_HOST="${2:-cmsweb-testbed.cern.ch}"

OUTPUT_BASE="${3:-test/materialized}"


# ------------------------------------------------------------
# Banner
# ------------------------------------------------------------

echo
echo "========================================"
echo " WMCore → DIRAC → CWL pipeline"
echo "========================================"
echo

echo "Request name : ${REQUEST_NAME}"
echo "CMS host     : ${CMS_HOST}"
echo "Output base  : ${OUTPUT_BASE}"
echo


# ------------------------------------------------------------
# Step 1
# ------------------------------------------------------------

echo "----------------------------------------"
echo "Step 1: Fetch WMCore workflow + translate to DIRAC IR"
echo "----------------------------------------"

python bin/wmc2transf.py \
  --fetch-inputs \
  --wmReqName "${REQUEST_NAME}" \
  --wmReqMgr "${CMS_HOST}" \
  --wmDasHost "https://${CMS_HOST}" \
  --output-base "${OUTPUT_BASE}"


# ------------------------------------------------------------
# Step 2
# ------------------------------------------------------------

echo
echo "----------------------------------------"
echo "Step 2: Run local transformation splitting"
echo "----------------------------------------"

TRANSFORMATION_FILE="$(find "${OUTPUT_BASE}/${REQUEST_NAME}/DIRAC.transf.d/Transformations" -maxdepth 1 -name '*.transformation.json' | head -n 1)"

if [ -z "${TRANSFORMATION_FILE}" ]; then
  echo "ERROR: no transformation file found under ${OUTPUT_BASE}/${REQUEST_NAME}/DIRAC.transf.d/Transformations"
  exit 1
fi

python bin/runLocalTransformation.py \
  --transformation-file "${TRANSFORMATION_FILE}"

# ------------------------------------------------------------
# Step 3
# ------------------------------------------------------------

echo
echo "----------------------------------------"
echo "Step 3: Export transformation bundle to CWL"
echo "----------------------------------------"

python bin/transf2cwl.py \
  --bundle-dir "${OUTPUT_BASE}/${REQUEST_NAME}/DIRAC.transf.d" \
  --output-base "${OUTPUT_BASE}"


# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

echo
echo "----------------------------------------"
echo "Pipeline finished"
echo "----------------------------------------"
echo

echo "Result directory:"
echo
echo "${OUTPUT_BASE}/${REQUEST_NAME}"
echo

echo "Main outputs:"
echo
echo "  WMCore serialization:"
echo "    ${OUTPUT_BASE}/${REQUEST_NAME}/WMCore.fetched.d"
echo
echo "  Local DIRAC materialization:"
echo "    ${OUTPUT_BASE}/${REQUEST_NAME}/DIRAC.transf.d"
echo
echo "  CWL bundle:"
echo "    ${OUTPUT_BASE}/${REQUEST_NAME}/DIRAC.cwl.d"
echo
