# Copyright (c) 2026
"""Versioned finite feature-recipe construction and two reviewed implementations.

Catalog expansion is a normal reviewed development operation. Enumeration knows
only compatibility metadata; executable support remains an explicit boundary.
Budgets bound one construction, not the lifetime vocabulary of this subsystem.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations
from uuid import UUID

from devtools.learning.measurement.contracts import nonempty
from devtools.learning.representation.features import FeatureTable, FeatureValueKind


def _hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode(),
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class FeatureOperator:
    """Reviewed definition metadata; possession does not load or execute code."""

    name: str
    version: int
    order: int
    input_semantics: str
    output_semantics: str
    incompatible_with: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        for v in (self.name, self.input_semantics, self.output_semantics):
            nonempty(v)
        if type(self.version) is not int or self.version < 1:
            msg = "positive operator version required"
            raise ValueError(msg)
        if type(self.order) is not int or self.order < 0:
            msg = "nonnegative canonical order required"
            raise ValueError(msg)
        if type(self.incompatible_with) is not tuple or len(
            set(self.incompatible_with),
        ) != len(self.incompatible_with):
            msg = "immutable unique incompatibility identities required"
            raise ValueError(msg)
        for name in self.incompatible_with:
            nonempty(name)

    @property
    def identity(self) -> str:
        """Apply the explicit identity contract within this owner."""
        return f"{self.name}_v{self.version}"


ORIGINAL_CONTINUOUS = "original_prepared_continuous_coordinates_v1"
SQUARES = FeatureOperator(
    "append_squared_features",
    1,
    0,
    ORIGINAL_CONTINUOUS,
    "append original x_i*x_i in original index order",
)
INTERACTIONS = FeatureOperator(
    "append_pairwise_interactions",
    1,
    1,
    ORIGINAL_CONTINUOUS,
    "append original x_i*x_j, i<j, lexicographic index order",
)
APPROVED_OPERATORS = (SQUARES, INTERACTIONS)


@dataclass(frozen=True, slots=True)
class FeatureRecipe:
    """Canonical nonempty operator subset with an explicit originating catalog."""

    catalog_identity: str
    operators: tuple[FeatureOperator, ...]
    construction_rule: str = "nonempty-compatible-subsets-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        nonempty(self.catalog_identity)
        if self.construction_rule != "nonempty-compatible-subsets-v1":
            msg = "unsupported construction rule"
            raise ValueError(msg)
        if type(self.operators) is not tuple or not self.operators:
            msg = "immutable nonempty recipe required"
            raise ValueError(msg)
        if any(not isinstance(o, FeatureOperator) for o in self.operators):
            msg = "typed operator definitions required"
            raise TypeError(msg)
        if len({o.identity for o in self.operators}) != len(self.operators):
            msg = "duplicate operator"
            raise ValueError(msg)
        if (
            tuple(sorted(self.operators, key=lambda o: (o.order, o.identity)))
            != self.operators
        ):
            msg = "noncanonical operator order"
            raise ValueError(msg)
        if any(o.input_semantics != ORIGINAL_CONTINUOUS for o in self.operators):
            msg = "incompatible original-coordinate inputs"
            raise ValueError(msg)
        if any(
            p.identity in o.incompatible_with
            for o in self.operators
            for p in self.operators
        ):
            msg = "incompatible operator subset"
            raise ValueError(msg)

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        return _hash(asdict(self))

    @property
    def identity(self) -> str:
        """Apply the explicit identity contract within this owner."""
        return "feature-recipe-v1:" + self.content_identity


@dataclass(frozen=True, slots=True)
class CandidateGeneration:
    """Finite construction receipt, including every unexecuted disposition."""

    approved_catalog: tuple[FeatureOperator, ...]
    catalog_identity: str
    candidate_budget: int
    maximum_operator_count_per_recipe: int
    recipes: tuple[FeatureRecipe, ...]
    omitted: tuple[tuple[str, str], ...]
    rejected: tuple[tuple[tuple[str, ...], str], ...]
    duplicate_definitions: tuple[str, ...]
    occurrence_id: UUID
    enumeration_budget: int
    construction_rule: str = "nonempty-compatible-subsets-v1"

    def __post_init__(self) -> None:
        """Validate the immutable scientific contract and its correspondence."""
        if (
            type(self.approved_catalog) is not tuple
            or not self.approved_catalog
            or any(not isinstance(o, FeatureOperator) for o in self.approved_catalog)
            or (
                tuple(
                    sorted(self.approved_catalog, key=lambda o: (o.order, o.identity)),
                )
                != self.approved_catalog
            )
            or (
                len({o.identity for o in self.approved_catalog})
                != len(self.approved_catalog)
            )
            or (
                self.catalog_identity
                != _hash([asdict(o) for o in self.approved_catalog])
            )
        ):
            msg = "canonical original approved catalog required"
            raise ValueError(msg)
        if any(
            type(v) is not int or v < 1
            for v in (
                self.candidate_budget,
                self.maximum_operator_count_per_recipe,
                self.enumeration_budget,
            )
        ):
            msg = "positive original construction budgets required"
            raise ValueError(msg)
        if (
            type(self.recipes) is not tuple
            or len(self.recipes) > self.candidate_budget
            or any(
                not isinstance(r, FeatureRecipe)
                or r.catalog_identity != self.catalog_identity
                or len(r.operators) > self.maximum_operator_count_per_recipe
                or any(o not in self.approved_catalog for o in r.operators)
                for r in self.recipes
            )
            or (len({r.identity for r in self.recipes}) != len(self.recipes))
        ):
            msg = "distinct compatible original generated recipes required"
            raise ValueError(msg)
        if (
            not isinstance(self.occurrence_id, UUID)
            or self.construction_rule != "nonempty-compatible-subsets-v1"
        ):
            msg = "original construction occurrence/rule required"
            raise ValueError(msg)
        if any(
            type(v) is not tuple
            for v in (self.omitted, self.rejected, self.duplicate_definitions)
        ):
            msg = "immutable construction dispositions required"
            raise ValueError(msg)

    @property
    def content_identity(self) -> str:
        """Apply the explicit content identity contract within this owner."""
        value = asdict(self)
        value["occurrence_id"] = str(self.occurrence_id)
        return _hash(value)


def generate_feature_recipes(
    approved: tuple[FeatureOperator, ...],
    *,
    candidate_budget: int,
    maximum_operator_count_per_recipe: int,
    occurrence_id: UUID,
    enumeration_budget: int = 4096,
) -> CandidateGeneration:
    """Enumerate by subset size then catalog order, with no outcome inputs.

    Definitions can expand without modifying enumeration. New executable behavior
    still requires an explicitly reviewed implementation. All budget omissions
    and incompatible subsets remain visible; truncated construction is not an
    exhaustive search. Exact repeated definitions are deduplicated visibly.
    """
    if (
        type(approved) is not tuple
        or not approved
        or any(not isinstance(o, FeatureOperator) for o in approved)
    ):
        msg = "explicit finite approved typed collection required"
        raise ValueError(msg)
    if any(
        type(v) is not int or v < 1
        for v in (
            candidate_budget,
            maximum_operator_count_per_recipe,
            enumeration_budget,
        )
    ):
        msg = "positive experiment budgets required"
        raise ValueError(msg)
    if not isinstance(occurrence_id, UUID):
        msg = "generation occurrence UUID required"
        raise TypeError(msg)
    unique: dict[str, FeatureOperator] = {}
    duplicates = []
    for operator in approved:
        if operator.identity in unique:
            if unique[operator.identity] != operator:
                msg = "contradictory operator version"
                raise ValueError(msg)
            duplicates.append(operator.identity)
        unique[operator.identity] = operator
    ordered = tuple(sorted(unique.values(), key=lambda o: (o.order, o.identity)))
    if (1 << len(ordered)) - 1 > enumeration_budget:
        msg = "catalog exceeds this construction's explicit enumeration budget"
        raise ValueError(msg)
    catalog = _hash([asdict(o) for o in ordered])
    recipes: list[FeatureRecipe] = []
    omitted: list[tuple[str, str]] = []
    rejected: list[tuple[tuple[str, ...], str]] = []
    for size in range(1, len(ordered) + 1):
        for subset in combinations(ordered, size):
            try:
                recipe = FeatureRecipe(catalog, subset)
            except ValueError as error:
                rejected.append((tuple((o.identity for o in subset)), str(error)))
                continue
            if size > maximum_operator_count_per_recipe:
                omitted.append((recipe.identity, "maximum_operator_count_per_recipe"))
            elif len(recipes) >= candidate_budget:
                omitted.append((recipe.identity, "candidate_budget"))
            else:
                recipes.append(recipe)
    return CandidateGeneration(
        ordered,
        catalog,
        candidate_budget,
        maximum_operator_count_per_recipe,
        tuple(recipes),
        tuple(omitted),
        tuple(rejected),
        tuple(duplicates),
        occurrence_id,
        enumeration_budget,
    )


def transform_features(
    original: FeatureTable,
    recipe: FeatureRecipe,
    *,
    maximum_dimension: int,
) -> FeatureTable:
    """Append only reviewed maps of ORIGINAL coordinates; never recurse.

    Neither arbitrary callables nor unknown operator definitions are executable.
    Resource bounds are supplied by the caller's authorized experiment.
    """
    if not isinstance(original, FeatureTable) or not isinstance(recipe, FeatureRecipe):
        msg = "typed original features and recipe required"
        raise TypeError(msg)
    if type(maximum_dimension) is not int or maximum_dimension < 1:
        msg = "positive dimension budget required"
        raise ValueError(msg)
    if not original.feature_names or any(
        k is not FeatureValueKind.CONTINUOUS for k in original.feature_value_kinds
    ):
        msg = "nonempty original continuous schema required"
        raise ValueError(msg)
    names = list(original.feature_names)
    pairs: list[tuple[int, int]] = []
    for operator in recipe.operators:
        if operator == SQUARES:
            added = [(i, i) for i in range(len(original.feature_names))]
        elif operator == INTERACTIONS:
            added = list(combinations(range(len(original.feature_names)), 2))
        else:
            msg = "operator has no approved executable implementation"
            raise ValueError(msg)
        if not added:
            msg = "operator produces no new coordinates for this input"
            raise ValueError(msg)
        pairs.extend(added)
        names.extend(
            (
                f"{operator.identity}[{i},{j}]:{original.feature_names[i]}*{original.feature_names[j]}"
                for i, j in added
            ),
        )
    if len(names) > maximum_dimension or len(set(names)) != len(names):
        msg = "expanded dimension/coordinate identities exceed compatibility"
        raise ValueError(msg)
    rows = tuple(
        tuple(row) + tuple((row[i] * row[j] for i, j in pairs)) for row in original.rows
    )
    if any(not math.isfinite(v) for row in rows for v in row):
        msg = "nonfinite transformed coordinate"
        raise ValueError(msg)
    return FeatureTable(tuple(names), rows, (FeatureValueKind.CONTINUOUS,) * len(names))
