# Lab 6 - REST vs. gRPC Measurements

All values are average milliseconds per operation. The REST and gRPC tests used 1,000 requests for localhost and same-zone measurements, and 100 requests for different-region measurements. PING values are average round-trip times from 10 packets.

| Method | Local (ms) | Same-Zone (ms) | Different Region (ms) |
|---|---:|---:|---:|
| REST add | 2.672 | 3.214 | 322.805 |
| gRPC add | 0.770 | 1.142 | 161.204 |
| REST rawimg | 5.199 | 7.817 | 1,291.375 |
| gRPC rawimg | 4.327 | 9.464 | 173.297 |
| REST dotproduct | 3.119 | 3.652 | 322.566 |
| gRPC dotproduct | 0.849 | 1.243 | 180.013 |
| REST jsonimg | 27.379 | 29.882 | 1,455.145 |
| gRPC jsonimg | 16.315 | 14.791 | 203.108 |
| PING | 0.036 | 0.376 | 158.339 |

## Observations

For localhost and same-zone calls, network latency was low and both APIs responded relatively quickly. gRPC was faster for `add` and `dotproduct` in both setups, although REST was faster for same-zone `rawimg` (7.817 ms versus 9.464 ms). The different-region measurements were much slower, consistent with the 158.339 ms average ping time between Oregon and Frankfurt. For example, REST `add` averaged 322.805 ms versus 161.204 ms for gRPC. The difference was even larger for image requests: REST `rawimg` averaged 1,291.375 ms versus 173.297 ms for gRPC, while REST `jsonimg` averaged 1,455.145 ms versus 203.108 ms for gRPC. Reusing a gRPC connection rather than creating a new REST HTTP connection for each call may explain some of this difference, but serialization and transfer costs may also contribute. JSON image requests were generally slower than raw-image requests, consistent with Base64 encoding and JSON processing overhead. Overall, gRPC performed better in these measurements, especially across regions. Bandwidth was not measured separately.
