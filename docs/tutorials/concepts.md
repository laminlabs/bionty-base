# Learn about concepts

In many practical applications, a biological entity (e.g., `Species`) represents a variable that can take values from a vocabulary of terms.

1. There are different roughly equivalent vocabularies for the same entity. For example, one can describe species with the vocabulary of the scientific names, the vocabulary of the common names, or the vocabulary of ontology IDs for the same species.
2. There are different versions and granularity of these vocabularies. Typically, vocabularies are based on a given version of a public ontology, and may contain “custom” terms representing new knowledge, that’s not yet represented publicly.

We address 1. with a so-called EntityTable model: Within Bionty, the primary representation for an entity is a EntityTable, in which each column of the EntityTable corresponds to a vocabulary.

We address 2. through a user-setup process consisting in

- looking up a standard ontology, fixing a resolution/depth of terms in the ontology and writing it to the vocabulary.
- adding user-defined terms to the ontology, or, if their relation within the ontology is not yet clear, directly to the vocabulary.

Example:

- Species is an entity.
- Take one value that the entity can take: _human_ is a choice (the common name) for a descriptor of the abstract entry/ value/ term _homo sapiens_
