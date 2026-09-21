# Orders and Samples in Confident

Orders and Samples are two core elements in Confident lab testing.
A sample is a single piece of material that is to be tested, and
an order is a collection of samples from one client that have been
requested for testing at the same time. Every sample always
belongs to exactly one order, and an order is always attached to
exactly one client and exactly one lab. Orders have a status that
represents the state of the order over time and is modified by
various actions detailed below. Understanding the different stages
of an order (and how this impacts the visibility of test results /
CoAs) is critical to providing a great user experience.

## Order Statuses

Each status has a numeric ID, used as the `status_id`
filter and returned by `GET /orderstatuses`.

- **Placed** (`status_id` 2) — By default, orders are created in
  the Placed stage, indicating that the client has requested the
  order but the lab has not yet validated the request nor taken
  custody of the samples.
- **In Progress** (`status_id` 3) — The lab has taken custody of
  the samples and is performing the required tests.
- **Completed** (`status_id` 4) — The order has been completed and
  all data for all samples is published to the client.
- **Canceled** (`status_id` 0) — The order has been canceled by
  the client or the lab. No more work will be done for this order or
  any sample in it.

## Order Actions

Actions are what move orders between the various statuses, as
shown below. The most important action is moving an order from In
Progress to Completed, since this is what converts all draft data
(test results, CoAs, and any additional documents) to published so
that it can be accessed by the client — read more in the Draft vs
Published Results section.

![Order lifecycle diagram](https://s3.amazonaws.com/confident-static/images/cc_order_lifecycle.svg)

The status-transition endpoints map to these actions:

| Action | Endpoint | Transition |
|---|---|---|
| Verify | [`POST /v0/labs/order/{order_id}/status/verify`](/v0/docs/labs/verify-order) | Placed → In Progress |
| Unverify | [`POST /v0/labs/order/{order_id}/status/unverify`](/v0/docs/labs/unverify-order) | In Progress → Placed |
| Complete | [`POST /v0/labs/order/{order_id}/status/complete`](/v0/docs/labs/complete-order) | In Progress → Completed |
| Revise | [`POST /v0/labs/order/{order_id}/status/revise`](/v0/docs/labs/revise-order) | Completed → In Progress |
| Cancel | [`POST /v0/labs/order/{order_id}/status/cancel`](/v0/docs/labs/cancel-order) | any (not cancelled) → Cancelled |
| Uncancel | [`POST /v0/labs/order/{order_id}/status/uncancel`](/v0/docs/labs/uncancel-order) | Cancelled → Placed |

## Draft vs Published Results/CoAs/Documents

It is important to understand that while test results and sample
documents are related to order status, they are
**not** directly controlled by it.

**All** client-facing pieces of information (test
results, CoAs, additional documents) in Confident work via a
draft system, meaning they are never visible to clients until
after the lab has an opportunity to review and then intentionally
publish them. Publishing happens for all draft info/files when the
sample's parent order is moved from In Progress to Completed
(which also delivers them to the client via email and potentially
other channels). Even after an order is in the Completed state,
any new data/files submitted to its samples will be drafts (i.e.,
not visible to the client) until the order is moved back to In
Progress and then moved to Completed again.

This draft/published state is usually denoted in the API with
fields that have the `_draft` suffix — this can be seen
via the
[`GET /v0/labs/sample/{sample_id}`](/v0/docs/labs/get-sample-details)
endpoint and the `has_lab_data`/`has_coa` vs
`has_lab_data_draft`/`has_coa_draft` fields.

### Detailed Example

| Step | Action | Draft Data/CoAs | Published Data/CoAs |
|---|---|---|---|
| 1 | Parent order created — sample XYZ is created | None | None |
| 2 | Parent order verified and moved to In Progress | None | None |
| 3 | Data A and CoA A submitted to sample | Data A, CoA A | None |
| 4 | Data B and CoA B submitted to sample (update with new results) | Data B, CoA B | None |
| 5 | Order completed — client notified | None | Data B, CoA B |
| 6 | Order revised (back to In Progress) — lab intends to adjust report | None | Data B, CoA B |
| 7 | Updated Data C and CoA C submitted to sample | Data C, CoA C | Data B, CoA B |
| 8 | Order completed again — client notified a second time | None | Data C, CoA C |

## Sample and Order Number Info

Sample and order numbers are generated automatically by Confident
when an order is created (or edited, in the case of adding samples
after an order is initially created). These numbers are generally
sequential (both are highly customizable with regard to format and
when numbers reset). Both order and sample numbers are always
globally unique and are the standard identifier used when
interacting with orders or samples from the API or the web
interface.

## Integration Suggestions

There are many different use cases for integrating with Confident
depending on how much interaction the lab wants to do in the LIMS
vs in the Confident web interface. When using Confident in the
most limited capacity (taking orders and generating all
results/CoAs in the LIMS and only submitting final,
ready-to-publish values and documents to Confident), you'll need
to make sure that you move orders to the Completed status at the
right time in your workflow in order to publish the correct
information. Most significantly, this means you must submit all
test results, Certificates of Analysis, and any other
documentation for **all** samples in an order
**before** it is moved to the Completed status. Doing
this in the wrong order will leave some of your data in the Draft
state and not deliver it correctly to the client. In this
situation we suggest creating orders in the In Progress status,
submitting everything for every sample in the order, and only then
moving the order to Completed. Please read the Draft vs Published
Results section for more details.

---

HTML version: https://api.confidentcannabis.com/v0/docs/order-lifecycle
