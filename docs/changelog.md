# Changelog

<!-- prettier-ignore -->
Name | PR | User | Date | Patch
--- | --- | --- | --- | ---
🚑 Fix lookup for empty strings | [314](https://github.com/laminlabs/bionty/pull/314) | [sunnyosun](https://github.com/sunnyosun) | 2023-04-23 | 0.11.6
⚡ Make sure no NAs present in the `entity.df.name` | [313](https://github.com/laminlabs/bionty/pull/313) | [sunnyosun](https://github.com/sunnyosun) | 2023-04-23 | 0.11.5
⬆️ Pronto>=2.5.4, removed cached_property dep for py3.7 | [312](https://github.com/laminlabs/bionty/pull/312) | [sunnyosun](https://github.com/sunnyosun) | 2023-04-23 |
⚡ Improve the speed loading of ontology df | [305](https://github.com/laminlabs/bionty/pull/305) | [sunnyosun](https://github.com/sunnyosun) | 2023-04-19 | 0.11.4
👷 Add staging to CI | [293](https://github.com/laminlabs/bionty/pull/293) | [Zethson](https://github.com/Zethson) | 2023-04-04 |
💚 Add current/lndb updating on new entities | [290](https://github.com/laminlabs/bionty/pull/290) | [Zethson](https://github.com/Zethson) | 2023-03-30 | 0.11.3
💚 Try fixing `lnschema-bionty` CI | [289](https://github.com/laminlabs/bionty/pull/289) | [falexwolf](https://github.com/falexwolf) | 2023-03-27 |
🐛 Fix reference_id for gene and protein | [288](https://github.com/laminlabs/bionty/pull/288) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-27 | 0.11.2
🚚 Renamed to reference_id everywhere | [287](https://github.com/laminlabs/bionty/pull/287) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-27 | 0.11.1
👷 Fix lnschema-bionty CI | [284](https://github.com/laminlabs/bionty/pull/284) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-27 |
🚚 Rename property `lookup_col` to `lookup_field` <span class="badge badge-warning">Breaking</span> | [283](https://github.com/laminlabs/bionty/pull/283) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-24 | 0.11.0
✅ Add update_defaults test | [280](https://github.com/laminlabs/bionty/pull/280) | [Zethson](https://github.com/Zethson) | 2023-03-23 |
👷 Test against `lnschema-bionty` | [279](https://github.com/laminlabs/bionty/pull/279) | [falexwolf](https://github.com/falexwolf) | 2023-03-23 |
✨ Move ID from Entity to curate <span class="badge badge-warning">Breaking</span> | [268](https://github.com/laminlabs/bionty/pull/268) | [Zethson](https://github.com/Zethson) | 2023-03-23 |
🐛 Fix removeprefix 3.8 & versions pathing | [277](https://github.com/laminlabs/bionty/pull/277) | [Zethson](https://github.com/Zethson) | 2023-03-22 | 0.10.1
📝 Updated the curation notebook for cellmarker | [274](https://github.com/laminlabs/bionty/pull/274) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-22 |
🍱 Updated CellMarker assets <span class="badge badge-warning">Breaking</span> | [271](https://github.com/laminlabs/bionty/pull/271) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-21 | 0.10.0
🚑 Ensure version names are strings | [269](https://github.com/laminlabs/bionty/pull/269) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-20 | 0.9.0
✨ Add pathway ontology | [267](https://github.com/laminlabs/bionty/pull/267) | [Zethson](https://github.com/Zethson) | 2023-03-17 | 0.9.0rc1
✨ Add compatibility functions | [264](https://github.com/laminlabs/bionty/pull/264) | [Zethson](https://github.com/Zethson) | 2023-03-17 |
✨ Add latest version inference if only db is passed | [256](https://github.com/laminlabs/bionty/pull/256) | [Zethson](https://github.com/Zethson) | 2023-03-14 |
🐛 Fix default ids | [257](https://github.com/laminlabs/bionty/pull/257) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-14 |
Add md5 sums | [249](https://github.com/laminlabs/bionty/pull/249) | [Zethson](https://github.com/Zethson) | 2023-03-13 |
🎨 Fixed case sensitivity, lookup output as namedtuple | [255](https://github.com/laminlabs/bionty/pull/255) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-11 |
💥 Lookup returns the full record <span class="badge badge-warning">Breaking</span> | [254](https://github.com/laminlabs/bionty/pull/254) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-11 |
💄 Actually fix image display | [253](https://github.com/laminlabs/bionty/pull/253) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-11 |
🐛 Fix img links | [252](https://github.com/laminlabs/bionty/pull/252) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-11 |
📝 Keep improving docs | [250](https://github.com/laminlabs/bionty/pull/250) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-11 |
🐛 Fix version order | [248](https://github.com/laminlabs/bionty/pull/248) | [Zethson](https://github.com/Zethson) | 2023-03-10 |
🐛 Ensure datadir is created | [245](https://github.com/laminlabs/bionty/pull/245) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-09 | 0.8.1
🐛 Fixed readout lookup | [244](https://github.com/laminlabs/bionty/pull/244) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-09 | 0.8.0
📝 A take on 3 summary bullets | [240](https://github.com/laminlabs/bionty/pull/240) | [falexwolf](https://github.com/falexwolf) | 2023-03-08 | 0.8rc2
💚 Fix CI build | [239](https://github.com/laminlabs/bionty/pull/239) | [sunnyosun](https://github.com/sunnyosun) | 2023-03-08 |
📝 Improving documentation | [220](https://github.com/laminlabs/bionty/pull/220) | [Zethson](https://github.com/Zethson) | 2023-03-08 |
👷 Add entity tests | [234](https://github.com/laminlabs/bionty/pull/234) | [Zethson](https://github.com/Zethson) | 2023-03-07 |
✨ Add names/website per ontology & improve versions rich tables | [232](https://github.com/laminlabs/bionty/pull/232) | [Zethson](https://github.com/Zethson) | 2023-03-06 |
📝 Add better docstrings and docstring decorator | [231](https://github.com/laminlabs/bionty/pull/231) | [Zethson](https://github.com/Zethson) | 2023-03-06 |
🐛 Fix cellmarker ontology | [230](https://github.com/laminlabs/bionty/pull/230) | [Zethson](https://github.com/Zethson) | 2023-03-03 | 0.8rc1
✨ Add CellLine ontology | [229](https://github.com/laminlabs/bionty/pull/229) | [Zethson](https://github.com/Zethson) | 2023-03-03 |
🎨 Simplify filenames | [227](https://github.com/laminlabs/bionty/pull/227) | [Zethson](https://github.com/Zethson) | 2023-03-03 |
🎨 Deduce filenames on the fly for non-S3 Entites | [223](https://github.com/laminlabs/bionty/pull/223) | [Zethson](https://github.com/Zethson) | 2023-03-01 |
📝 Simplify FAQ | [218](https://github.com/laminlabs/bionty/pull/218) | [Zethson](https://github.com/Zethson) | 2023-02-27 |
🎨 Simplify ontology accesses | [217](https://github.com/laminlabs/bionty/pull/217) | [Zethson](https://github.com/Zethson) | 2023-02-27 |
🎨 Move Species to Entity | [216](https://github.com/laminlabs/bionty/pull/216) | [Zethson](https://github.com/Zethson) | 2023-02-27 |
🎨 Rename EntityTable to Entity <span class="badge badge-warning">Breaking</span> | [214](https://github.com/laminlabs/bionty/pull/214) | [Zethson](https://github.com/Zethson) | 2023-02-26 |
🎨 Add laminci | [213](https://github.com/laminlabs/bionty/pull/213) | [Zethson](https://github.com/Zethson) | 2023-02-26 |
✨ Add HCA ontology | [209](https://github.com/laminlabs/bionty/pull/209) | [Zethson](https://github.com/Zethson) | 2023-02-21 |
✨ Improve version handling | [202](https://github.com/laminlabs/bionty/pull/202) | [Zethson](https://github.com/Zethson) | 2023-02-21 |
🔥 No downloading upon import | [205](https://github.com/laminlabs/bionty/pull/205) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-20 |
👷 Remove py3.7 from CI | [206](https://github.com/laminlabs/bionty/pull/206) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-20 |
📝 Add better documentation & function to print currently available/active ontologies | [201](https://github.com/laminlabs/bionty/pull/201) | [Zethson](https://github.com/Zethson) | 2023-02-17 |
👷 Add HDO & improve support for multiple databases | [187](https://github.com/laminlabs/bionty/pull/187) | [Zethson](https://github.com/Zethson) | 2023-02-15 |
👷 Add GH workflow to check for version URLs | [188](https://github.com/laminlabs/bionty/pull/188) | [Zethson](https://github.com/Zethson) | 2023-02-13 | 0.7.0
⬆️ Rename `lndb_setup` to `lndb` | [189](https://github.com/laminlabs/bionty/pull/189) | [bpenteado](https://github.com/bpenteado) | 2023-02-13 |
✨ Add human phenotype ontology | [172](https://github.com/laminlabs/bionty/pull/172) | [Zethson](https://github.com/Zethson) | 2023-02-06 |
📝 Add dev APIs to docs | [183](https://github.com/laminlabs/bionty/pull/183) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-06 |
📝 Use guide/index as landing page | [182](https://github.com/laminlabs/bionty/pull/182) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-06 |
🔥 Removed _logger.py | [176](https://github.com/laminlabs/bionty/pull/176) | [sunnyosun](https://github.com/sunnyosun) | 2023-02-06 |
🐛 Fix #167 | [168](https://github.com/laminlabs/bionty/pull/168) | [Zethson](https://github.com/Zethson) | 2023-02-05 |
👷 Add lamindocs secret key for CI | [173](https://github.com/laminlabs/bionty/pull/173) | [Zethson](https://github.com/Zethson) | 2023-02-05 |
✨ Added case_sensitive to curate | [169](https://github.com/laminlabs/bionty/pull/169) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-31 | 0.6.5
🚑 Fix version key type | [166](https://github.com/laminlabs/bionty/pull/166) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-18 | 0.6.4
🚚 Rename species common_name to name | [165](https://github.com/laminlabs/bionty/pull/165) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-17 | 0.6.3
🎨 Changed version filename separator from | to ___ | [164](https://github.com/laminlabs/bionty/pull/164) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-16 | 0.6.2
🐛 Fix docs | [162](https://github.com/laminlabs/bionty/pull/162) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-12 | 0.6.1
👷 Expand CI to python 3.7-3.10 | [161](https://github.com/laminlabs/bionty/pull/161) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-12 | 0.6.0
✨ Pull species table dynamically from Ensembl | [160](https://github.com/laminlabs/bionty/pull/160) | [sunnyosun](https://github.com/sunnyosun) | 2023-01-05 |
✨ Add progressbar to downloads | [159](https://github.com/laminlabs/bionty/pull/159) | [Zethson](https://github.com/Zethson) | 2023-01-05 |
🐛 Fixed id=name bug | [157](https://github.com/laminlabs/bionty/pull/157) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-09 | 0.5.7
♻️ Refactor version files | [156](https://github.com/laminlabs/bionty/pull/156) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-08 | 0.5.6
✨ Added ontology_info | [155](https://github.com/laminlabs/bionty/pull/155) | [sunnyosun](https://github.com/sunnyosun) | 2022-12-01 |
✨ Add readout to lookup | [153](https://github.com/laminlabs/bionty/pull/153) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-24 | 0.5.5
✨ Write most recent versions to `_current.yaml` | [152](https://github.com/laminlabs/bionty/pull/152) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-23 |
🎨 Fetch the latest ontology from ols | [151](https://github.com/laminlabs/bionty/pull/151) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-22 |
🚚 Moved readout from bioreadout into bionty | [150](https://github.com/laminlabs/bionty/pull/150) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-19 |
✨ Added a local versions tracking file | [149](https://github.com/laminlabs/bionty/pull/149) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-18 |
🐛 Fixed column id in curate | [148](https://github.com/laminlabs/bionty/pull/148) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-16 | 0.5.4
🩹 Removed prefix in ontology df | [147](https://github.com/laminlabs/bionty/pull/147) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-15 | 0.5.3
🎨 Default id to ontology_id | [146](https://github.com/laminlabs/bionty/pull/146) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-15 |
🚚 Rename id to ontology_id for ontology df | [145](https://github.com/laminlabs/bionty/pull/145) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-11 | 0.5.2
⚡ Cache id and name for ontology | [144](https://github.com/laminlabs/bionty/pull/144) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-10 |
🎨 Simplified ontology | [143](https://github.com/laminlabs/bionty/pull/143) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-10 |
🐛 Fixed bug in tissue id | [142](https://github.com/laminlabs/bionty/pull/142) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-10 |
⚡ Switch to cloudpath for caching | [141](https://github.com/laminlabs/bionty/pull/141) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-09 |
⚡ Cache species table | [140](https://github.com/laminlabs/bionty/pull/140) | [sunnyosun](https://github.com/sunnyosun) | 2022-11-06 | 0.5.1
📝 Link the species df to bionty-assets | [139](https://github.com/laminlabs/bionty/pull/139) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-25 | 0.5.0
🍱 Updated protein table | [138](https://github.com/laminlabs/bionty/pull/138) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-25 |
🍱 Updated cell marker link | [137](https://github.com/laminlabs/bionty/pull/137) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-25 |
🍱 Updated the species df path to use s3 | [136](https://github.com/laminlabs/bionty/pull/136) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-25 | 0.4.3
🍱 Updated gene table | [135](https://github.com/laminlabs/bionty/pull/135) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-25 |
🚚 Migrated the tables to the new ids | [134](https://github.com/laminlabs/bionty/pull/134) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-24 | 0.4.2
🔥 Removed `feature_model` lookups | [133](https://github.com/laminlabs/bionty/pull/133) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-20 | 0.4.1
💥 Redefine `lookup` in `EntityTable` | [132](https://github.com/laminlabs/bionty/pull/132) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-12 | 0.4.0
🎨 Improve `todict()`, added to `EntityTable` | [131](https://github.com/laminlabs/bionty/pull/131) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-11 | 0.3.2
🐛 Fix duplicated cell marker names | [130](https://github.com/laminlabs/bionty/pull/130) | [sunnyosun](https://github.com/sunnyosun) | 2022-10-03 | 0.3.1
🍱 Added `description` and `version` columns to the gene table | [128](https://github.com/laminlabs/bionty/pull/128) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-27 | 0.3.0
🚚 Migrated dfs of gene, protein, cell marker to the lndb version | [127](https://github.com/laminlabs/bionty/pull/127) | [sunnyosun](https://github.com/sunnyosun) | 2022-09-26 | 0.2.5
🚚 Rename guides to FAQ, tutorials to guide | [125](https://github.com/laminlabs/bionty/pull/125) | [falexwolf](https://github.com/falexwolf) | 2022-09-05 |
🔥 Remove cell_type, disease from lookup | [123](https://github.com/laminlabs/bionty/pull/123) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-29 | 0.2.4
🚚 Rename `cell_marker` column to `name` to fit schema | [122](https://github.com/laminlabs/bionty/pull/122) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-28 | 0.2.3
🚚 Rename gene_symbol to symbol | [121](https://github.com/laminlabs/bionty/pull/121) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-28 | 0.2.2
🔥 Remove `lookup.cell_marker` | [120](https://github.com/laminlabs/bionty/pull/120) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-28 |
🎨 Fixed bugs in ontology class | [119](https://github.com/laminlabs/bionty/pull/119) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-28 | 0.2.1
🚚 Moved `.entity` to the base class | [118](https://github.com/laminlabs/bionty/pull/118) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-27 |
📝 Updated docs etc | [117](https://github.com/laminlabs/bionty/pull/117) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-27 |
✅ Added more tests | [116](https://github.com/laminlabs/bionty/pull/116) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-27 |
✨ Added `Tissue` entity | [115](https://github.com/laminlabs/bionty/pull/115) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-27 |
✨ Added `CellMarker` entity | [114](https://github.com/laminlabs/bionty/pull/114) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-26 | 0.2.0
🚚 Updated protein df, rename `name` to `gene_symbol` | [113](https://github.com/laminlabs/bionty/pull/113) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-26 |
📝 Added lookup to the API ref | [112](https://github.com/laminlabs/bionty/pull/112) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-25 |
🔊 Added `n_mapped` to logging | [111](https://github.com/laminlabs/bionty/pull/111) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-18 | 0.1.11
🚚 Rename gene_ids to gene_id | [110](https://github.com/laminlabs/bionty/pull/110) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-18 | 0.1.10
🎨 Migrate to ensembl gene reference | [109](https://github.com/laminlabs/bionty/pull/109) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-18 |
🎨 Ensure `entrez_gene_id` is `int` | [108](https://github.com/laminlabs/bionty/pull/108) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-16 |
⚡ Use display_name as common_name so that its unique | [107](https://github.com/laminlabs/bionty/pull/107) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-15 |
🩹 Increased timeout | [106](https://github.com/laminlabs/bionty/pull/106) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-11 | 0.1.9
🩹 Modify `get_term` | [104](https://github.com/laminlabs/bionty/pull/104) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-10 | 0.1.8
✨ Use pronto to access cell type ontology | [103](https://github.com/laminlabs/bionty/pull/103) | [sunnyosun](https://github.com/sunnyosun) | 2022-08-08 | 0.1.7
🐛 Fixed duplicated index during curate | [100](https://github.com/laminlabs/bionty/pull/100) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-31 | 0.1.6
✨ Added `lookup` module for lookups | [98](https://github.com/laminlabs/bionty/pull/98) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-31 | 0.1.5
🔥 Removed duplicated code in lookup | [97](https://github.com/laminlabs/bionty/pull/97) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-28 | 0.1.4
✨ Added shortcuts for looking up static sets | [96](https://github.com/laminlabs/bionty/pull/96) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-28 | 0.1.3
🔥 Switched logger to use lamin-logger | [95](https://github.com/laminlabs/bionty/pull/95) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-23 |
✨ Allow to input columns with non-standard names | [93](https://github.com/laminlabs/bionty/pull/93) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-11 | 0.1.2
✨ Maps alias when using gene symbols | [92](https://github.com/laminlabs/bionty/pull/92) | [sunnyosun](https://github.com/sunnyosun) | 2022-07-06 |
🎨  Added a developer API | [89](https://github.com/laminlabs/bionty/pull/89) | [falexwolf](https://github.com/falexwolf) | 2022-07-02 | 0.1.1
✅ Add more tests for curation, rename `Table` to `EntityTable` | [88](https://github.com/laminlabs/bionty/pull/88) | [falexwolf](https://github.com/falexwolf) | 2022-07-02 |
♻️ Refactor curation | [87](https://github.com/laminlabs/bionty/pull/87) | [falexwolf](https://github.com/falexwolf) | 2022-07-02 |
📝 Prototype index standardization | [86](https://github.com/laminlabs/bionty/pull/86) | [falexwolf](https://github.com/falexwolf) | 2022-07-02 |
🎨 Polish APIs and tutorials | [85](https://github.com/laminlabs/bionty/pull/85) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-30 |
✨ Added MGI for mouse genes, switched to use feather for HGNC | [84](https://github.com/laminlabs/bionty/pull/84) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-29 |
🍱 Added back the Protein entity | [83](https://github.com/laminlabs/bionty/pull/83) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-29 |
🚚 Move hard-to-test code from bionty into asset curation | [82](https://github.com/laminlabs/bionty/pull/82) | [falexwolf](https://github.com/falexwolf) | 2022-06-28 |
🏗️ Simplify Bionty | [81](https://github.com/laminlabs/bionty/pull/81) | [falexwolf](https://github.com/falexwolf) | 2022-06-28 |
🚸 Pull disease data from bionty-assets | [80](https://github.com/laminlabs/bionty/pull/80) | [falexwolf](https://github.com/falexwolf) | 2022-06-27 |
🚸 Replace HGNC file access with our S3 bucket | [79](https://github.com/laminlabs/bionty/pull/79) | [falexwolf](https://github.com/falexwolf) | 2022-06-26 |
✅ Added disease and tissue to quickstart | [78](https://github.com/laminlabs/bionty/pull/78) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-26 |
👷 Update coverage setup | [77](https://github.com/laminlabs/bionty/pull/77) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-26 |
✅ Collect coverage from test nbs | [76](https://github.com/laminlabs/bionty/pull/76) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-26 |
💄 Added badges for build, codecov, pypi, pre-commit  | [75](https://github.com/laminlabs/bionty/pull/75) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-25 |
👷 Added Codecov to the build.yml | [73](https://github.com/laminlabs/bionty/pull/73) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-25 |
📝 Iterate quickstart for better readability | [71](https://github.com/laminlabs/bionty/pull/71) | [falexwolf](https://github.com/falexwolf) | 2022-06-24 |
💥 Improved quickstart, implemented .dataclass everywhere | [67](https://github.com/laminlabs/bionty/pull/67) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-22 | 0.1.0
🔥 Remove versioneer | [66](https://github.com/laminlabs/bionty/pull/66) | [falexwolf](https://github.com/falexwolf) | 2022-06-22 |
⚡ Implemented pickling of dataclasses, refactored static class into `.dataclass` | [65](https://github.com/laminlabs/bionty/pull/65) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-22 | 0.1a3
🚚 Renamed Celltype to CellType, fixed gene Entry fields | [62](https://github.com/laminlabs/bionty/pull/62) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-17 | 0.1a2
📝 Rewrite landing page and rename tasks | [61](https://github.com/laminlabs/bionty/pull/61) | [falexwolf](https://github.com/falexwolf) | 2022-06-17 |
✨ Added static class `gene` | [59](https://github.com/laminlabs/bionty/pull/59) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-16 |
💄 Prettified ontology docstring | [58](https://github.com/laminlabs/bionty/pull/58) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-15 |
🔨 `Species` class by default taks a `common_name` | [56](https://github.com/laminlabs/bionty/pull/56) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-13 |
♻️ Refactored `species` | [55](https://github.com/laminlabs/bionty/pull/55) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-13 | 0.1a1
♻️ Refactored `species` | [54](https://github.com/laminlabs/bionty/pull/54) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-13 |
⚡ Speed up requests with `async` | [53](https://github.com/laminlabs/bionty/pull/53) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-12 |
💚 Fix docs build warnings/errors | [52](https://github.com/laminlabs/bionty/pull/52) | [falexwolf](https://github.com/falexwolf) | 2022-06-10 |
♻️ Refactored `species` for dual usage | [51](https://github.com/laminlabs/bionty/pull/51) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-10 |
🚚 Rename `taxon` to `species` | [50](https://github.com/laminlabs/bionty/pull/50) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-10 |
🎨 Made `Ensembl` its own class | [45](https://github.com/laminlabs/bionty/pull/45) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-09 |
✨ Propose new design of the entity APIs | [44](https://github.com/laminlabs/bionty/pull/44) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-07 |
🐛 Fix `gene.id` fields | [43](https://github.com/laminlabs/bionty/pull/43) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-03 |
🐛 Fix `standardize` to work on any iterables | [41](https://github.com/laminlabs/bionty/pull/41) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-03 |
🎨 Implement an initial `.standardize()` in the `Ontology` manager | [40](https://github.com/laminlabs/bionty/pull/40) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-02 |
✨ Introduce `tissue` | [38](https://github.com/laminlabs/bionty/pull/38) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-01 |
✨ Introduce `disease` | [36](https://github.com/laminlabs/bionty/pull/36) | [sunnyosun](https://github.com/sunnyosun) | 2022-06-01 |
✨ Introduce `celltype` | [34](https://github.com/laminlabs/bionty/pull/34) | [sunnyosun](https://github.com/sunnyosun) | 2022-05-30 |
