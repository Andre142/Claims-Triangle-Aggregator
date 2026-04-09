# Claims-Triangle-Aggregator

An automated Python data pipeline built to ingest raw, transactional insurance claims data and generate cumulative run-off triangles.

This tool was built using pandas and tested against the Kasa.ai Simulation Machine dataset by Gabrielli & Wüthrich (100,000 records of non-life claims).

## Parameters

Segment Filtering: Pass dictionary arguments (e.g., segment_filter={'lob': 3}) to subset the data by Line of Business, Claim Code, or Injury Type before aggregation.

Accounting Basis (Occurrence vs. Claims-Made): Toggle the origin period between accident_year (Occurrence) and calculated report_year (Claims-Made) by adding the report lag to the origin date.

Time Cohorts: Toggle between annual and quarterly origin periods for development tracking.

Metric Toggles: Switch between paid and incurred/reported loss metrics.
