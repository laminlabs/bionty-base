# Guide

Welcome to the Bionty guide! 👋

In the following we will outline the main concepts and terminology of Bionty.

## Entities

In many practical applications, a biological entity (e.g., `Species`) represents a variable that can take values from a vocabulary of terms.

1. There are different roughly equivalent vocabularies for the same entity.
   For example, one can describe species with the vocabulary of the scientific names, the vocabulary of the common names,
   or the vocabulary of ontology IDs for the same species.
2. There are different versions and granularity of these vocabularies.
   Typically, vocabularies are based on a given version of a public ontology,
   and may contain “custom” terms representing new knowledge that is not yet represented publicly.

## Entity model

We address 1. with a so-called `Entity` model: Within Bionty, the primary representation for an entity is an `Entity` object,
in which each column of the Entity table attribute corresponds to a vocabulary.

We address 2. through a user-setup process consists of:

- looking up a standard ontology, fixing a resolution/depth of terms in the ontology and writing it to the vocabulary.
- adding user-defined terms to the ontology, or, if their relation within the ontology is not yet clear, directly to the vocabulary.

Example:

- Species is an entity.
- Take one value that the entity can take: _human_ is a choice (the name) for a descriptor of the abstract entry/ value/ term _homo sapiens_

## Glossary

1. **entity** (lower case) refers to biological entities as described above.
2. **`Entity`** refers to the entity class.
3. **Entity table/reference table** refers to a table where the columns are vocabularies, accessed via `Entity.df`.
4. **Records** refers to entries/rows in the Entity table.
5. **Vocabularies** are sets of terms that describe an entity.
6. **Ontologies** refer to sets of standardized terms that constitute a vocabulary.

```{toctree}
:maxdepth: 2
:hidden:

lookup
ontology
curate
config
extend
```
