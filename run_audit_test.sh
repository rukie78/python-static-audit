#!/bin/bash

# Example test run for the audit script
echo "Running static audit on example project..."
python3 audit_en_full.py . || echo "Audit script failed to run"

echo "Done. Check the generated report file (audit_report_*.txt)"
