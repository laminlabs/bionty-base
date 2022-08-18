# Changelog

<!-- prettier-ignore -->
Name | PR | User | Date | Patch
--- | --- | --- | --- | ---
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
