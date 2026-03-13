# Markdown Style Guide

This guide defines the Markdown rendering conventions used in this
repository.

It is based on actual rendering behavior observed in:

- GitHub Markdown
- Firefox ESR
- the browser interface used during development

## 1. Diagrams must use explicit fenced code blocks

Long diagrams must always be enclosed in explicit fenced code blocks.

Preferred:

- use a fenced block with the entire diagram inside it
- keep the whole diagram in one block

Not reliable:

- indentation-only code blocks
- partially fenced long diagrams

Reason:

If indentation changes or a non-indented line appears, Markdown may
terminate the block early and the remainder of the diagram will break.

## 2. Box-drawing diagrams are allowed

Box-drawing characters render correctly in GitHub Markdown code blocks
when fenced properly.

Allowed examples include:

```
- ┌ ┐ └ ┘
- │ ─
- ▼
```

These are preferred for architecture diagrams because they are more
readable than plain ASCII fallbacks.

## 3. Every connector line must have a destination

When drawing architecture diagrams:

- every vertical line must terminate in a box or node
- every branch line must connect to an actual downstream element
- no decorative or mirrored dangling lines should remain

## 4. Keep central and runtime branches distinct

When drawing execution architecture:

- central workflow description/export steps stay in the central layer
- runtime execution steps stay in the runtime layer

Applied to this repository:

- data discovery belongs inside the translator
- CWL export is a sibling branch of DIRAC materialization
- CWL export is not a runtime step

## 5. Prefer dash-based Markdown lists

Use this style for lists:

- top-level item
  - nested item
  - nested item
- next top-level item

Do not use bullet glyphs such as:

- •

## 6. Preserve narrow, readable line lengths

To reduce rendering issues:

- avoid overly wide paragraphs
- wrap prose manually
- keep diagram width reasonable

## 7. Avoid HTML-like placeholders in code blocks

Do not write placeholders like:

- `<outdir>`
- `<task>`
- `<input>`

Use instead:

- OUTDIR
- TASK_NAME
- INPUT_DIR

Reason:

Some renderers may treat HTML-like tokens specially.

## 8. Repository convention for diagrams

Use this general pattern:

- heading
- short explanatory sentence
- one fenced block containing the whole diagram

Keep explanatory prose outside the fenced block unless it is part of the
diagram itself.

## 9. Current architectural conventions

For this project, diagrams should reflect:

- WMCore.fetched.d
- DIRAC.transf.d
- DIRAC.cwl.d

and the following architectural choices:

- data discovery is part of the translator
- CWL export is a central sibling branch
- runtime flows continue only through DIRAC materialization

## 10. Diagram review checklist

Before committing a diagram:

- verify the whole diagram is inside one explicit fenced block
- verify alignment in GitHub preview
- verify no connector line terminates in empty space
- verify central and runtime branches are not mixed
