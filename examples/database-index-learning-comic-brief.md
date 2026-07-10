# Example Brief: Database Index Learning Comic

## Goal
Create a six-page Korean educational comic that helps working software engineers understand why database indexes make some reads faster, why they do not help every query, and what tradeoffs they impose on writes and storage.

## Deliverable Type
- `adult-learning-comic`

## Audience
- Backend and product engineers with 1-5 years of experience
- Comfortable with SQL but not expected to know B+tree internals
- Adult professional tone with enough mechanism to guide index decisions

## Learning Intent
- Surface belief: "Adding an index makes database queries faster."
- Corrected mental model: An index is a query-shaped, ordered access path that reduces page reads for some predicates while adding maintenance and storage costs.
- Practical transfer: Given a query pattern, the reader can explain whether an index is likely to help and name one cost to check.
- Page budget: 6

## Required Facts
- Database storage is read in pages/blocks rather than one logical row at a time.
- A B+tree index narrows the search through ordered internal nodes and keeps searchable entries in leaf nodes.
- Composite index usefulness depends on column order and query predicates.
- Low selectivity can make a full scan cheaper than using an index.
- Indexes add storage and write-maintenance cost.
- Exact behavior depends on the database engine and optimizer; avoid universal performance guarantees.

## Desired Visual Direction
- Bright professional data lab rendered as a polished Korean educational webtoon
- Recurring adult database reliability engineer, product engineer, and compact database-page mascot
- White page base, black panel borders, teal/blue structure diagrams, coral warning accents
- Character scenes alternate with B+tree, data-page, range-scan, and write-cost diagrams

## Text Policy
- `dialogue-baked`
- Exact Korean titles, panel labels, short/medium speech bubbles, SQL fragments, and diagram labels
- Full source citations stay in the footer or handoff rather than dense illustrated panels

## Constraints
- Six portrait 3:4 pages
- Four or five panels per page
- `gpt-image-2`
- Render character sheet first and use it as the identity reference for all six pages
