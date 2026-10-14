# GERMLINE Antibody Corpus — INDEX

**100 antibodies** across **17 projects** — generated 2026-10-14T20:47:10+00:00 from ARVO v3.0.0.

> Status: 🟢 2 validated (double-checked on a real runner) · 🟡 98 draft — full run log in `VERIFICATION.md`.

## ffmpeg (14)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000015` | asan | Heap-buffer-overflow READ {*} | Medium | `9a9034958aec` | [link](https://issues.oss-fuzz.com/issues/42470347) |
| 🟡 `AB-000016` | asan | Global-buffer-overflow READ 4 | Medium | `85a921f46184` | [link](https://issues.oss-fuzz.com/issues/42470362) |
| 🟡 `AB-000017` | asan | Stack-buffer-underflow WRITE 2 | Medium | `25eb10d941f3` | [link](https://issues.oss-fuzz.com/issues/42470719) |
| 🟡 `AB-000018` | asan | Stack-buffer-overflow READ {*} | Medium | `25eb10d941f3` | [link](https://issues.oss-fuzz.com/issues/42470722) |
| 🟡 `AB-000019` | asan | Global-buffer-overflow READ 4 | Medium | `85a921f46184` | [link](https://issues.oss-fuzz.com/issues/42470801) |
| 🟡 `AB-000020` | asan | Global-buffer-overflow READ 2 | Medium | `e90f0ac334f2` | [link](https://issues.oss-fuzz.com/issues/42470870) |
| 🟡 `AB-000021` | asan | UNKNOWN READ | Medium | `ab160efa2850` | [link](https://issues.oss-fuzz.com/issues/42472617) |
| 🟡 `AB-000022` | ubsan | UNKNOWN WRITE | High | `ab160efa2850` | [link](https://issues.oss-fuzz.com/issues/42472621) |
| 🟡 `AB-000023` | asan | UNKNOWN WRITE | High | `ab160efa2850` | [link](https://issues.oss-fuzz.com/issues/42472627) |
| 🟡 `AB-000024` | asan | Heap-buffer-overflow READ 4 | Medium | `fcbda8af175a` | [link](https://issues.oss-fuzz.com/issues/42472718) |
| 🟡 `AB-000025` | asan | Heap-buffer-overflow WRITE 2 | High | `1f686d023b95` | [link](https://issues.oss-fuzz.com/issues/42473419) |
| 🟡 `AB-000026` | ubsan | Heap-buffer-overflow WRITE 8 | High | `ce551a3925a1` | [link](https://issues.oss-fuzz.com/issues/42473850) |
| 🟡 `AB-000027` | ubsan | Index-out-of-bounds | Medium | `1002932a3b16` | [link](https://issues.oss-fuzz.com/issues/42473861) |
| 🟡 `AB-000028` | asan | Heap-buffer-overflow READ 1 | Medium | `d227ed5d5983` | [link](https://issues.oss-fuzz.com/issues/42473874) |

## libxml2 (14)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟢 `AB-000001` | msan | Use-of-uninitialized-value | Medium | `074180119fc9` | [link](https://issues.oss-fuzz.com/issues/42470114) |
| 🟢 `AB-000002` | msan | Use-of-uninitialized-value | Medium | `074180119fc9` | [link](https://issues.oss-fuzz.com/issues/42470125) |
| 🟡 `AB-000003` | asan | Heap-use-after-free READ 1 | High | `8c9daf790abf` | [link](https://issues.oss-fuzz.com/issues/42470339) |
| 🟡 `AB-000004` | asan | Heap-use-after-free READ 1 | High | `8c9daf790abf` | [link](https://issues.oss-fuzz.com/issues/42470348) |
| 🟡 `AB-000005` | asan | Bad-free | Medium | `1567b55b72b8` | [link](https://issues.oss-fuzz.com/issues/42471662) |
| 🟡 `AB-000006` | asan | Heap-double-free | High | `26828cb3a129` | [link](https://issues.oss-fuzz.com/issues/42472675) |
| 🟡 `AB-000007` | ubsan | Index-out-of-bounds | Medium | `474967241cdc` | [link](https://issues.oss-fuzz.com/issues/42475106) |
| 🟡 `AB-000008` | asan | Heap-use-after-free READ 8 | High | `664f881008f4` | [link](https://issues.oss-fuzz.com/issues/42478580) |
| 🟡 `AB-000009` | asan | Stack-buffer-overflow WRITE {*} | High | `932cc9896ab4` | [link](https://issues.oss-fuzz.com/issues/42480782) |
| 🟡 `AB-000010` | asan | Heap-use-after-free READ 2 | High | `2af3c2a8b974` | [link](https://issues.oss-fuzz.com/issues/42484562) |
| 🟡 `AB-000011` | asan | Heap-use-after-free READ 4 | High | `dba82a8c0453` | [link](https://issues.oss-fuzz.com/issues/42486565) |
| 🟡 `AB-000012` | asan | Heap-use-after-free READ 8 | High | `19cae17f5a2a` | [link](https://issues.oss-fuzz.com/issues/42486665) |
| 🟡 `AB-000013` | asan | Heap-use-after-free READ 4 | High | `ba589adc2f86` | [link](https://issues.oss-fuzz.com/issues/42486883) |
| 🟡 `AB-000014` | ubsan | Bad-cast | High | `bfd2f4300fb3` | [link](https://issues.oss-fuzz.com/issues/42496802) |

## imagemagick (12)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000029` | msan | Use-of-uninitialized-value | Medium | `cfd2824f02b6` | [link](https://issues.oss-fuzz.com/issues/42470067) |
| 🟡 `AB-000030` | asan | Heap-buffer-overflow READ 8 | Medium | `9bd3e4c89ccb` | [link](https://issues.oss-fuzz.com/issues/42470131) |
| 🟡 `AB-000031` | msan | Use-of-uninitialized-value | Medium | `33c60b6e5111` | [link](https://issues.oss-fuzz.com/issues/42470554) |
| 🟡 `AB-000032` | asan | Heap-buffer-overflow READ 1 | Medium | `9177b7b3c278` | [link](https://issues.oss-fuzz.com/issues/42472424) |
| 🟡 `AB-000033` | asan | UNKNOWN READ | Medium | `07eebcd72f45` | [link](https://issues.oss-fuzz.com/issues/42472871) |
| 🟡 `AB-000034` | msan | UNKNOWN READ | Medium | `07eebcd72f45` | [link](https://issues.oss-fuzz.com/issues/42472880) |
| 🟡 `AB-000035` | ubsan | Index-out-of-bounds | Medium | `df835cab0576` | [link](https://issues.oss-fuzz.com/issues/42472890) |
| 🟡 `AB-000036` | asan | Heap-buffer-overflow READ 8 | Medium | `7921e3f13b72` | [link](https://issues.oss-fuzz.com/issues/42473518) |
| 🟡 `AB-000037` | asan | Heap-buffer-overflow READ 4 | Medium | `75477483fbf9` | [link](https://issues.oss-fuzz.com/issues/42473556) |
| 🟡 `AB-000038` | asan | Heap-use-after-free WRITE 4 | High | `f7206618d27c` | [link](https://issues.oss-fuzz.com/issues/42474040) |
| 🟡 `AB-000039` | asan | Heap-buffer-overflow READ 1 | Medium | `58b1d87bef2b` | [link](https://issues.oss-fuzz.com/issues/42474313) |
| 🟡 `AB-000040` | asan | Stack-buffer-overflow READ 8 | Medium | `cdddf99e151c` | [link](https://issues.oss-fuzz.com/issues/42475836) |

## harfbuzz (10)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000041` | asan | Heap-buffer-overflow READ 8 | Medium | `2dde6c803a9e` | [link](https://issues.oss-fuzz.com/issues/42470093) |
| 🟡 `AB-000042` | asan | Stack-use-after-return READ 1 | Medium | `2dde6c803a9e` | [link](https://issues.oss-fuzz.com/issues/42470094) |
| 🟡 `AB-000043` | asan | Heap-buffer-overflow READ 8 | Medium | `2dde6c803a9e` | [link](https://issues.oss-fuzz.com/issues/42470096) |
| 🟡 `AB-000044` | msan | Use-of-uninitialized-value | Medium | `2dde6c803a9e` | [link](https://issues.oss-fuzz.com/issues/42470110) |
| 🟡 `AB-000045` | asan | Heap-buffer-overflow READ 1 | Medium | `67449c39331b` | [link](https://issues.oss-fuzz.com/issues/42470379) |
| 🟡 `AB-000046` | asan | Heap-buffer-overflow READ 4 | Medium | `f8ccb545c47a` | [link](https://issues.oss-fuzz.com/issues/42470383) |
| 🟡 `AB-000047` | asan | Heap-buffer-overflow READ 1 | Medium | `f8ccb545c47a` | [link](https://issues.oss-fuzz.com/issues/42470395) |
| 🟡 `AB-000048` | msan | Use-of-uninitialized-value | Medium | `f8ccb545c47a` | [link](https://issues.oss-fuzz.com/issues/42470405) |
| 🟡 `AB-000049` | asan | UNKNOWN READ | Medium | `5c65ed800de4` | [link](https://issues.oss-fuzz.com/issues/42470841) |
| 🟡 `AB-000050` | ubsan | UNKNOWN READ | Medium | `ca54eba4846d` | [link](https://issues.oss-fuzz.com/issues/42470990) |

## curl (8)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000051` | ubsan | Null-dereference READ | Medium | `78d5302b5c05` | [link](https://issues.oss-fuzz.com/issues/42470017) |
| 🟡 `AB-000052` | asan | UNKNOWN READ | Medium | `f3ce38739fa4` | [link](https://issues.oss-fuzz.com/issues/42472402) |
| 🟡 `AB-000053` | asan | Negative-size-param | Medium | `65fda739ee35` | [link](https://issues.oss-fuzz.com/issues/42477423) |
| 🟡 `AB-000054` | msan | Use-of-uninitialized-value | Medium | `65fda739ee35` | [link](https://issues.oss-fuzz.com/issues/42477424) |
| 🟡 `AB-000055` | msan | Use-of-uninitialized-value | Medium | `84ced9389e1a` | [link](https://issues.oss-fuzz.com/issues/42477426) |
| 🟡 `AB-000056` | asan | Negative-size-param | Medium | `65fda739ee35` | [link](https://issues.oss-fuzz.com/issues/42477432) |
| 🟡 `AB-000057` | asan | Heap-buffer-overflow READ 1 | Medium | `65fda739ee35` | [link](https://issues.oss-fuzz.com/issues/42477466) |
| 🟡 `AB-000058` | asan | Heap-use-after-free READ 6 | High | `02c6b984cb7a` | [link](https://issues.oss-fuzz.com/issues/42478820) |

## wireshark (7)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000059` | asan | Heap-buffer-overflow READ 1 | Medium | `38657fad5803` | [link](https://issues.oss-fuzz.com/issues/42470183) |
| 🟡 `AB-000060` | asan | Heap-buffer-overflow READ 1 | Medium | `38657fad5803` | [link](https://issues.oss-fuzz.com/issues/42470194) |
| 🟡 `AB-000061` | asan | Global-buffer-overflow READ 4 | Medium | `895ad30b5a18` | [link](https://issues.oss-fuzz.com/issues/42470895) |
| 🟡 `AB-000062` | ubsan | Index-out-of-bounds | Medium | `895ad30b5a18` | [link](https://issues.oss-fuzz.com/issues/42470900) |
| 🟡 `AB-000063` | asan | Global-buffer-overflow READ 8 | Medium | `d9231144b652` | [link](https://issues.oss-fuzz.com/issues/42470925) |
| 🟡 `AB-000064` | asan | UNKNOWN READ | Medium | `d9231144b652` | [link](https://issues.oss-fuzz.com/issues/42470929) |
| 🟡 `AB-000065` | ubsan | UNKNOWN READ | Medium | `d9231144b652` | [link](https://issues.oss-fuzz.com/issues/42470973) |

## ghostpdl (6)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000066` | asan | Null-dereference READ | Medium | `77f79475fd04` | [link](https://issues.oss-fuzz.com/issues/42477726) |
| 🟡 `AB-000067` | asan | Heap-use-after-free READ 8 | High | `6fc5cbc5bc57` | [link](https://issues.oss-fuzz.com/issues/42481819) |
| 🟡 `AB-000068` | asan | Segv on unknown address | Medium | `d703f355af52` | [link](https://issues.oss-fuzz.com/issues/42482668) |
| 🟡 `AB-000069` | asan | UNKNOWN READ | Medium | `748edd2fd75c` | [link](https://issues.oss-fuzz.com/issues/42483325) |
| 🟡 `AB-000070` | asan | Heap-use-after-free WRITE 4 | High | `7861fcad13c4` | [link](https://issues.oss-fuzz.com/issues/42492999) |
| 🟡 `AB-000071` | asan | Stack-use-after-return WRITE 8 | Medium | `20610dc28ee3` | [link](https://issues.oss-fuzz.com/issues/42496125) |

## libarchive (5)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000077` | asan | Heap-buffer-overflow WRITE 1 | High | `b52dd6c9e4ef` | [link](https://issues.oss-fuzz.com/issues/42471116) |
| 🟡 `AB-000078` | asan | Heap-buffer-overflow READ 1 | Medium | `4bc5892128a0` | [link](https://issues.oss-fuzz.com/issues/42471319) |
| 🟡 `AB-000079` | asan | Stack-buffer-overflow WRITE 7 | High | `4bd12b6f40cb` | [link](https://issues.oss-fuzz.com/issues/42472727) |
| 🟡 `AB-000080` | asan | Heap-buffer-overflow READ 1 | Medium | `3614747af54e` | [link](https://issues.oss-fuzz.com/issues/42473117) |
| 🟡 `AB-000081` | asan | Heap-buffer-overflow READ {*} | Medium | `39736c43bd73` | [link](https://issues.oss-fuzz.com/issues/42473801) |

## php-src (5)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000072` | asan | Heap-buffer-overflow READ 1 | Medium | `1806ce9cb019` | [link](https://issues.oss-fuzz.com/issues/42478840) |
| 🟡 `AB-000073` | msan | Use-of-uninitialized-value | Medium | `9ed82b1f7b17` | [link](https://issues.oss-fuzz.com/issues/42480628) |
| 🟡 `AB-000074` | msan | Use-of-uninitialized-value | Medium | `b5e004379647` | [link](https://issues.oss-fuzz.com/issues/42480756) |
| 🟡 `AB-000075` | asan | Heap-use-after-free READ 4 | High | `fd08f062ae5a` | [link](https://issues.oss-fuzz.com/issues/42481412) |
| 🟡 `AB-000076` | asan | Heap-use-after-free READ 4 | High | `7e2bd95fa5fb` | [link](https://issues.oss-fuzz.com/issues/42481430) |

## binutils-gdb (4)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000086` | asan | Global-buffer-overflow READ 8 | Medium | `66a66a17f489` | [link](https://issues.oss-fuzz.com/issues/42479120) |
| 🟡 `AB-000087` | asan | Stack-buffer-overflow WRITE 1 | High | `bbf9a0b5eef3` | [link](https://issues.oss-fuzz.com/issues/42479123) |
| 🟡 `AB-000088` | asan | Global-buffer-overflow READ 4 | Medium | `dee334510fe3` | [link](https://issues.oss-fuzz.com/issues/42479126) |
| 🟡 `AB-000089` | asan | Global-buffer-overflow READ 4 | Medium | `66a66a17f489` | [link](https://issues.oss-fuzz.com/issues/42479130) |

## gpac (4)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000082` | asan | Segv on unknown address | Medium | `b03c9f252526` | [link](https://issues.oss-fuzz.com/issues/42494317) |
| 🟡 `AB-000083` | asan | Heap-buffer-overflow READ 9 | Medium | `758135e91e62` | [link](https://issues.oss-fuzz.com/issues/42494318) |
| 🟡 `AB-000084` | asan | Heap-buffer-overflow READ 4 | Medium | `322c8a92e3d3` | [link](https://issues.oss-fuzz.com/issues/42494345) |
| 🟡 `AB-000085` | asan | Stack-use-after-return WRITE 4 | Medium | `82396cfa523b` | [link](https://issues.oss-fuzz.com/issues/42494354) |

## freetype2 (3)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000090` | msan | Use-of-uninitialized-value | Medium | `94ebc248653e` | [link](https://issues.oss-fuzz.com/issues/42475209) |
| 🟡 `AB-000091` | asan | Heap-buffer-overflow WRITE 8 | High | `edf401485450` | [link](https://issues.oss-fuzz.com/issues/42490980) |
| 🟡 `AB-000092` | asan | Heap-buffer-overflow READ 8 | Medium | `e9a154e70015` | [link](https://issues.oss-fuzz.com/issues/42499092) |

## openssl (3)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000093` | asan | Stack-use-after-return READ 4 | Medium | `83b4a24384e6` | [link](https://issues.oss-fuzz.com/issues/42475667) |
| 🟡 `AB-000094` | asan | Heap-buffer-overflow WRITE 1 | High | `ed57f7f93508` | [link](https://issues.oss-fuzz.com/issues/42476770) |
| 🟡 `AB-000095` | asan | Heap-buffer-overflow READ 14 | Medium | `aec9667bd19a` | [link](https://issues.oss-fuzz.com/issues/42478556) |

## libwebp (2)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000096` | asan | Negative-size-param | Medium | `277d30749f15` | [link](https://issues.oss-fuzz.com/issues/42498407) |
| 🟡 `AB-000097` | asan | UNKNOWN READ | Medium | `e542fc7a8a26` | [link](https://issues.oss-fuzz.com/issues/42500241) |

## libpng (1)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000099` | asan | Heap-buffer-overflow WRITE {*} | High | `357af1f09532` | [link](https://issues.oss-fuzz.com/issues/42498959) |

## libtiff (1)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000100` | msan | Use-of-uninitialized-value | Medium | `0f013e5b5a55` | [link](https://issues.oss-fuzz.com/issues/42489909) |

## zlib (1)

| Antibody | Sanitizer | Crash type | Severity | Fix | Report |
|---|---|---|---|---|---|
| 🟡 `AB-000098` | msan | Use-of-uninitialized-value | Medium | `981ee7570ad9` | [link](https://issues.oss-fuzz.com/issues/42514310) |
