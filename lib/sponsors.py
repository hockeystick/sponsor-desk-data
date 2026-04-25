"""Sponsor folders: profile, press releases, past partnerships, 2026 priorities.

Content is written by hand as static English strings — not templated —
because the four sponsors are a fixed cast and scale-of-one realism
beats scale-of-N generation. A banned-phrase filter runs before every
write; if anything smells like corporate boilerplate or LLM-generic
output, the run aborts.

Each profile.md opens with a disclosure note: every sponsor is a
fictional analogue of a real PNW or national company. The names are
designed to read plausibly as a Portland-metro sponsor while not
claiming any actual entity has run these activities.
"""
from __future__ import annotations

import random
from pathlib import Path

from lib.sponsors_new import (
    _existing_leadership,
    bull_run_cider,
    cascadia_outfitters_coop,
    lewis_clark_foundation,
    meyer_northwest_trust,
    onpoint_cooperative,
    pacific_northwest_health,
    pacific_tower_development,
    portland_museum_of_art,
    reed_college_press,
    travel_oregon,
)

# English LLM-sludge tells. Hits abort the run.
_BANNED_PHRASES: tuple[str, ...] = (
    "at the intersection of",
    "in today's rapidly evolving",
    "in an ever-changing world",
    "ever-changing landscape",
    "rapidly evolving landscape",
    "leverage", "leveraging",
    "synergy", "synergies",
    "best-in-class",
    "world-class",
    "cutting-edge",
    "game-changing",
    "paradigm shift",
    "revolutionize",
    "revolutionizing",
    "seamless", "seamlessly",
    "we're committed to",
    "we are committed to",
    "our mission is to",
    "passionate about",
    "thought leader",
    "thought leadership",
    "robust ecosystem",
    "vibrant ecosystem",
    "unlock the potential",
    "unlocking the potential",
)


def _check_banned(text: str, source_label: str) -> None:
    lowered = text.lower()
    hits = [p for p in _BANNED_PHRASES if p in lowered]
    if hits:
        raise RuntimeError(
            f"banned phrase in {source_label}: {hits!r}. "
            "fix the copy — don't weaken the filter."
        )


_DISCLOSURE = (
    "_This sponsor is a fictional analogue. Names, leadership, programs, "
    "and figures are invented for synthetic-data purposes and are not "
    "affiliated with any real company or organization._"
)


# ---- Portland General Energy ------------------------------------------------

_PGE: dict[str, str] = {
"profile.md": f"""\
# Portland General Energy

{_DISCLOSURE}

Portland General Energy is the dominant electric utility serving the
Portland metropolitan area, with approximately 870,000 residential
and commercial customer accounts across Multnomah, Washington,
Clackamas, Marion, Polk, and Yamhill counties. The company was formed
in its current shape from a 1968 utility merger and has operated as
a publicly traded investor-owned utility since 1986.

## Operations

Portland General Energy generates electricity from a mixed portfolio:
hydroelectric (Pelton-Round Butte, Sullivan Plant), wind (Tucannon
River, Biglow Canyon), natural gas (Beaver, Coyote Springs), and a
declining share of coal contracted from out-of-state plants. The
company is on a state-mandated path to 100% emissions-free
electricity by 2040 under HB 2021.

Key programs in current operation:

- **Bright Future Resilience Program**: a $1.4 billion grid-hardening
  initiative announced in 2024, focused on undergrounding lines in
  high-fire-risk wildland-urban-interface areas and installing
  additional sectionalizing devices in eastern Multnomah County.
- **Drive EV Now**: customer rebates and Level 2 charger installation
  support for residential and small-business customers. Active in 14
  Oregon ZIP codes; expanded to East Portland in 2025.
- **Solar Plus Storage**: residential solar with optional battery
  backup, available under a community-aggregated billing model with
  EnergyTrust of Oregon.
- **Income-Qualified Bill Discount**: a 25% discount applied
  automatically to verified low-income residential accounts.

## Leadership

- **Sara Holloway**, Chief Executive Officer. Joined Portland General
  Energy as VP of Power Operations in 2014 and was named CEO in 2022.
  Holds a BS in electrical engineering from Oregon State and an MBA
  from Willamette University.
- **Vincent Chau**, Vice President for Public Policy and Regulatory
  Affairs. Previously deputy general counsel for the Oregon Public
  Utility Commission.
- **Carmen Delgado**, Vice President for Communications. Previously
  director of communications at Travel Oregon.

## Position on contested issues

Portland General Energy maintains a public position on rate-setting
that is, by its own framing, "uncomfortable but necessary." The
company filed a 7.4% rate increase in September 2025 — a request that
drew sharp editorial pushback from regional outlets including The
Cascade Tribune. CEO Sara Holloway, in a December 2025 statement,
reaffirmed the company's support for the Public Utility Commission's
stakeholder review process and acknowledged that the timing of the
filing — coming nine months after a damaging summer-reliability
report — was difficult. The company has stated it will accept any
adjusted rate the PUC orders, including an outcome below the
requested 7.4%.

On grid resilience: a 2024 internal review (publicly released in
February 2025 under a state public-records ruling) identified
delayed maintenance on three eastern Multnomah County substations
that contributed to summer 2024 outages. Portland General Energy has
publicly accepted the review's findings and pledged a 24-month
remediation plan that is currently halfway complete.

On sponsorship: Portland General Energy maintains an editorial
firewall policy for all sponsored journalism it underwrites. The
company has, on two occasions in 2024–2025, declined to sponsor
specific articles on rate-related topics where editorial concluded
the firewall could not be cleanly maintained.
""",

"brand_priorities_2026.md": f"""\
# 2026 Brand Priorities — Portland General Energy

{_DISCLOSURE}

_Internal document shared with regional media partners and civic
stakeholders. Approved by the Communications Committee, January 2026._

Portland General Energy's 2026 communications agenda reflects a clear
operational reality: the company is in the middle of a complex grid
transition while also operating under heightened public scrutiny on
both rates and reliability. The priorities below acknowledge that
context rather than try to talk past it.

## 1. Talk honestly about what the rate filing pays for

The 7.4% rate request — currently before the PUC — funds three
specific work streams: substation modernization in eastern Multnomah
County, the second phase of Bright Future Resilience, and the Drive
EV Now infrastructure build-out. Our 2026 communications need to
clearly link each dollar to what it does. Vague references to
"reliability investment" do not satisfy customer or editorial
audiences. Where the case is weak, we should say so.

## 2. Continue the Drive EV Now build-out in East Portland

Drive EV Now expanded into East Portland in March 2025 after
sustained criticism that earlier rollouts had concentrated on
higher-income ZIP codes. The 2026 build-out target is 1,200
additional Level 2 installations in the four eastside neighborhoods
identified as priority by the Portland Bureau of Planning's
equitable-electrification analysis.

## 3. Be the subject of journalism we don't pay for

Portland General Energy will continue to underwrite The Cascade
Tribune's climate desk under a multi-year underwriting agreement
that explicitly does not cover any rate-related coverage. We expect
and accept that editorial will continue to publish critical pieces
on our rate filings, our grid performance, and our generation mix.
The point of underwriting is not to buy quiet.

## 4. Publish reliability data quarterly, in the open

Beginning Q2 2026, Portland General Energy will publish circuit-level
SAIDI and SAIFI data quarterly, including substation maintenance
status, on an open data portal accessible without an account. The
data will lag operations by 30 days. This satisfies a December 2025
PUC stakeholder ask and replaces our previous practice of releasing
the same data only annually and on request.

## 5. Direct outreach to Latino customers in East Portland

Bilingual customer service is now a baseline expectation. Our 2026
add: bilingual outreach for the income-qualified bill discount
program, which is reaching only 41% of the customers identified as
likely eligible. The gap is concentrated in Spanish-speaking
households in East Portland and Forest Grove.

## What we will not do

- We will not pursue a corporate rebrand in 2026, despite a
  recommendation from outside consultants. The rate filing is not the
  moment.
- We will not run brand campaigns that minimize the operational
  challenges in our 100% emissions-free transition. Honest
  storytelling builds more trust than aspirational statements.
- We will not extend underwriting relationships to outlets that
  cannot maintain editorial firewalls.
""",

"past_media_partnerships.md": f"""\
# Media Partnerships — Portland General Energy

{_DISCLOSURE}

Portland General Energy partners with regional media on three
formats: long-running underwriting agreements, sponsored sections
with strict editorial firewalls, and event co-presenting. The
company does not buy display advertising on news sites. Listed
below are partnerships from the last 18 months relevant to outlets
considering similar arrangements.

## OPB — Energy & Environment Underwriting

A multi-year underwriting agreement with Oregon Public Broadcasting
that funds the energy and environment desk's reporting capacity. The
agreement specifies that no content produced under the desk's
editorial direction is subject to sponsor review. OPB has published
multiple pieces critical of Portland General Energy under this
arrangement; the underwriting has not been pulled or threatened.

Annual commitment: $180,000.

## Willamette Week — Sustainability Series Co-Production

A 2025 sponsored section that ran across six weeks in spring 2025,
co-produced by Willamette Week's editorial team. Topics included
residential heat-pump conversion, the economics of EV adoption for
working families, and a feature on EnergyTrust of Oregon. Editorial
control sat with Willamette Week. Portland General Energy's
involvement was limited to providing data, customer interviews
(with subjects' consent), and the funding commitment.

What worked: the topical scope was tightly defined in advance and
both teams stayed inside it. The section avoided rate-related
coverage, which would have created firewall problems.

What didn't: post-campaign measurement was inconsistent because
Willamette Week and Portland General Energy used different
attribution frameworks. We've since standardized on a shared
reporting template.

Six-week budget: $42,000.

## Portland Center Stage — Annual Series Sponsor

Annual presenting sponsorship of Portland Center Stage's main-stage
series since 2022. This is brand presence, not journalism — Portland
General Energy is acknowledged in playbills and on PCS's website.
Renewed for 2026.

Annual commitment: $90,000.

## Pickathon — Community Stage Co-Sponsor

Portland General Energy co-sponsored Pickathon's Community Stage in
2024 and 2025. The sponsorship covers the festival's accessibility
program and on-site EV charging deployment. Renewing for 2026 with
expanded scope.

Annual commitment: $35,000.

## Partnerships we have declined

In 2024–2025 Portland General Energy declined six proposed media
partnerships, primarily on firewall grounds: outlets that could not
demonstrate independent editorial control over content the company
might be referenced in, or that proposed campaigns where the
boundary between sponsored content and editorial coverage of rate
matters was insufficiently clear.
""",

"press_releases/2024-11-14-annual-reliability-report.md": f"""\
# Portland General Energy publishes 2024 annual reliability report, acknowledges summer outage failures

*Portland, Oregon — November 14, 2024.* Portland General Energy
published its 2024 annual reliability report on Thursday, opening
with an unusually direct acknowledgment that the company's
performance during the August 2024 heat dome fell short of its own
service standards. The report, audited by an independent engineering
firm under terms set by the Oregon Public Utility Commission, is
available in full on the company's open-data portal.

"We had three substations on the eastern edge of our service
territory that were not in the condition our customers had a right
to expect," CEO Sara Holloway said in a statement accompanying the
report. "The August outages were not the result of unprecedented
weather. They were the result of maintenance backlog. We're
publishing this report in the form we are because customers are
owed a clear account."

The report identifies three specific substations — Linnemann,
Damascus, and Sandy Boulevard — where preventive maintenance had
slipped behind the company's internal schedule. During the August
heat event, two of the three experienced equipment failures that
contributed to a combined 41,000 customer outages, with the longest
sustained outage lasting 19 hours.

Portland General Energy committed to a 24-month remediation plan
that includes accelerated maintenance on 17 additional substations
identified by the audit, replacement of approximately 380 aging
distribution transformers, and the installation of 220 additional
sectionalizing devices in high-fire-risk areas. The remediation
plan, with quarterly milestones, will be filed with the PUC by
December 15, 2024.

The company also disclosed that internal correspondence about
maintenance backlog dating to 2023 has been provided to the PUC's
investigative staff under the commission's standing-information
requirements, and to two news organizations under public-records
requests. Portland General Energy did not contest either disclosure.

"We are not here to manage perception," said Vincent Chau, the
company's Vice President for Public Policy. "We're here to fix the
substations and report progress in public."

The full reliability report, including circuit-level SAIDI and SAIFI
data, is available at pge-energy.com/reliability-2024.

*Press contact: Carmen Delgado, VP Communications,
press@pge-energy.com, (503) 555-0142.*
""",

"press_releases/2025-04-22-drive-ev-east-portland.md": f"""\
# Portland General Energy expands Drive EV Now charger installation program to East Portland

*Portland, Oregon — April 22, 2025.* Portland General Energy
announced today that its Drive EV Now residential charger
installation program will expand into East Portland beginning in
May, with an initial deployment target of 1,200 Level 2 home
chargers across the four neighborhoods identified by the Portland
Bureau of Planning's equitable-electrification analysis: Lents,
Powellhurst-Gilbert, Centennial, and Hazelwood.

The expansion responds to sustained criticism — from the City of
Portland, customer advocacy groups, and several news organizations
including The Cascade Tribune — that the program's earlier rollouts
had concentrated installations in higher-income ZIP codes in
Southwest Portland and Lake Oswego.

"The earlier criticism was right," CEO Sara Holloway said at a
launch event held at the Portland Mercado on Foster Boulevard. "Our
first 1,800 installations were not where the equity case was
strongest. The 2025 build-out fixes that, and we expect future
build-outs to start in the neighborhoods where the case is the
strongest, not the easiest."

The expanded program offers eligible East Portland residential
customers a Level 2 charger and standard installation at no
out-of-pocket cost, with the company recovering the cost over time
through a small per-kWh adjustment to vehicle-charging electricity
usage. Eligibility is open to any single-family residential customer
in the four target neighborhoods regardless of income.

Portland General Energy partnered with three local electrical
contracting firms — including two minority-owned firms identified
through the City of Portland's Prosper Portland small-business
program — for the installation work. The company has committed
that at least 60% of installation labor for the East Portland
build-out will go to firms in those neighborhoods.

The expanded program is funded under the Drive EV Now component of
Portland General Energy's 2024 rate case, which is not part of the
separate 2025 rate filing currently under PUC review.

Customers can check eligibility and request an installation visit
at pge-energy.com/drive-ev-now or by calling the program hotline at
(503) 555-0177.

*Press contact: Carmen Delgado, VP Communications,
press@pge-energy.com.*
""",

"press_releases/2025-09-08-rate-case-filing.md": f"""\
# Portland General Energy files 7.4% rate increase request with Oregon PUC

*Portland, Oregon — September 8, 2025.* Portland General Energy
filed a general rate case with the Oregon Public Utility Commission
this morning requesting a 7.4% increase in residential electricity
rates, citing investments in grid resilience, the second phase of
the Bright Future Resilience program, and continued build-out of
the Drive EV Now charger network.

The request, if approved at the level filed, would add an estimated
$11.20 to a typical residential customer's monthly bill. The PUC's
review process is expected to extend through the first half of
2026, with public comment periods scheduled in November 2025 and
February 2026.

"Filing a rate increase nine months after publishing the
reliability report we did is uncomfortable, and we want to
acknowledge that directly," CEO Sara Holloway said. "We considered
phasing the request differently. We concluded that customers are
better served by us filing the case now, in full, with the
investments laid out, rather than splitting it into smaller
increments that would obscure what's actually being paid for."

The company released a detailed breakdown of the request alongside
the filing. Approximately $340 million of the rate base increase is
attributed to the substation modernization and grid-hardening work
identified in the November 2024 reliability report. An additional
$210 million is attributed to the Bright Future Resilience program's
wildland-urban-interface undergrounding. The remainder is split
across the Drive EV Now infrastructure build-out, the company's
share of contracted hydroelectric maintenance, and rising operating
costs.

Portland General Energy acknowledged in the filing that consumer
advocacy groups, including the Citizens' Utility Board of Oregon,
are likely to contest the request. The company committed to making
all underlying engineering and cost data available for public review
through the PUC's docket and to participating in the commission's
stakeholder workshops.

"We expect a tough review, and we accept whatever rate the
commission orders, including a rate below what we requested,"
Holloway said.

The full rate case filing is available on the PUC's docket and at
pge-energy.com/rate-case-2025.

*Press contact: Carmen Delgado, VP Communications,
press@pge-energy.com.*
""",

"press_releases/2026-02-19-cfo-cso-appointments.md": f"""\
# Portland General Energy names new Chief Financial Officer and Chief Sustainability Officer

*Portland, Oregon — February 19, 2026.* Portland General Energy
announced two senior leadership appointments today: Patricia
Sandoval as Chief Financial Officer, effective March 1, and Linda
Park as Chief Sustainability Officer, a newly created C-suite
position effective immediately.

Sandoval joins Portland General Energy from Avista Corporation in
Spokane, where she served as Senior Vice President and Treasurer
for six years. Before Avista, she held finance roles at PacifiCorp
and worked at Deloitte's energy practice. She holds an MBA from
University of Washington and a BA from Whitman College.

Park is internally promoted from her prior role as Vice President
for Resource Planning. The Chief Sustainability Officer position
consolidates oversight of the company's HB 2021 emissions
trajectory, the Bright Future Resilience program, and the Drive EV
Now build-out under a single executive. Park has been with Portland
General Energy since 2018.

"This is a structural decision," CEO Sara Holloway said. "Our
sustainability commitments and our investment commitments cannot
sit in different reporting lines. They have to be planned together,
and they have to be answerable to a single executive. That executive
is Linda."

The appointments follow a December 2025 board review that
recommended consolidating sustainability oversight and recruiting a
CFO with deep regulatory-utility experience. Both appointments were
made by the company's Board of Directors after a four-month search
process led by Spencer Stuart.

Portland General Energy also announced that Vincent Chau, Vice
President for Public Policy, will lead the company's response to
the November 2025 PUC stakeholder review of the company's 7.4%
rate case. The PUC is expected to issue its order on the rate case
in May or June 2026.

*Press contact: Carmen Delgado, VP Communications,
press@pge-energy.com.*
""",
}


# ---- Powell's Community Foundation ------------------------------------------

_POWELLS_CF: dict[str, str] = {
"profile.md": f"""\
# Powell's Community Foundation

{_DISCLOSURE}

Powell's Community Foundation is an independent 501(c)(3) cultural
philanthropy headquartered in Portland, Oregon. The foundation was
endowed in 2018 with $120 million in initial assets — half from the
Powell family's personal philanthropic vehicle, half from matching
contributions from a regional consortium of donors. The foundation
operates fully independently of Powell's Books, the bookstore
chain; the two organizations share a name and historical connection
but no governance, staff, or financial overlap.

## Programmatic focus

The foundation's grantmaking concentrates on four areas, with
programmatic budgets approved annually by the board:

- **K–12 literacy programs**: support for school librarians,
  classroom-library purchasing for Title I schools, and after-school
  reading programs across the Portland Public Schools district and
  partner districts in East Multnomah County.
- **Independent publishing**: grants to small presses and literary
  magazines based in Oregon and Washington. The 2025 cycle awarded
  $1.4 million across 24 publishers.
- **Local journalism support**: pass-through grants to independent
  Oregon news organizations for civic and cultural reporting,
  administered with editorial firewalls maintained by the
  recipient organization.
- **Library access**: support for branch operations at Multnomah
  County Library and Hood River County Library, focused on Sunday
  hours and bilingual programming.

In 2025 the foundation moved $14.2 million in grants and
program-related investments. It maintains a five-year spending
target of 5.5–6.0% of corpus, slightly above the IRS minimum.

## Leadership

- **Margaret Hsu**, Executive Director since 2021. Previously
  director of the Wallace Foundation's arts education program;
  before that, deputy director at Literary Arts in Portland. Holds
  a PhD in education policy from the University of Oregon.
- **Jonathan Forsythe**, Director of Programs. Previously program
  officer at the Meyer Memorial Trust.
- **Anjali Mehta**, Chief Financial Officer.

The foundation's board is composed of nine voting members, including
two Powell family representatives, two K–12 educators (currently a
PPS librarian and a teacher in the David Douglas school district),
and five at-large members appointed for staggered three-year terms.

## Position on contested issues

In late 2024 a small but vocal group, organized as Parents First
Oregon, mounted a campaign objecting to a Powell's Community
Foundation–funded K–12 reading list that included three titles by
LGBTQ+ authors. The group submitted formal complaints to the
foundation's board and to the Oregon Department of Education and
distributed a petition that gathered 4,200 signatures.

The foundation's board, after a 90-day review process that included
public comment, voted in March 2025 to maintain the original reading
list without changes. Executive Director Margaret Hsu, in a
statement at the time, framed the decision as one of editorial
independence: "Reading lists curated by educators are educator
decisions. The foundation's role is to fund, not to curate. We will
not establish a precedent of removing titles from a list because a
funder received complaints about them."

The decision drew counter-criticism from a different direction:
several long-time donors expressed concern that the foundation had
not consulted them adequately during the review process. The
foundation's board adopted a revised stakeholder consultation
protocol in May 2025 that clarifies when and how donors will be
informed about controversies — without giving donors any role in
program decisions.

The foundation continues to fund all three of the contested titles
in subsequent grant cycles.
""",

"brand_priorities_2026.md": f"""\
# 2026 Programmatic Priorities — Powell's Community Foundation

{_DISCLOSURE}

_Approved by the Powell's Community Foundation Board of Trustees,
December 2025. Released as part of the foundation's annual public
reporting._

The foundation's 2026 priorities reflect a deliberate continuation
of the program lines established in the 2024–2026 strategic plan,
with two specific expansions and one structural reform.

## 1. K–12 literacy: continue and expand the school-librarian fund

The foundation's School Librarian Fund — which provides direct
salary support for librarian positions in Title I schools that have
lost librarian funding through district budget cuts — will expand
from 12 funded positions in 2025 to 18 funded positions in 2026.
The expansion adds positions in three David Douglas schools and
three schools in the Reynolds school district. Each position is
funded at full FTE for the 2026–27 academic year, with a renewable
three-year commitment.

## 2. Independent publishing: launch a Pacific Northwest small-press
   sustainability fund

A new program line in 2026, with $1.8 million committed for the
year. The fund makes operating grants — not project grants — to
small presses based in Oregon and Washington with annual revenue
under $500,000. Operating support is the form of philanthropy that
small presses report needing most and that they receive least, and
the foundation believes operating grants better serve the long
trajectory of these organizations than project-by-project funding.

## 3. Local journalism support: open new application cycle in March

The foundation's local journalism program — a pass-through grant
mechanism that supports civic and cultural reporting at independent
Oregon news organizations — will open its 2026 application cycle in
March. Grant size will range from $25,000 to $90,000. The 2026
cycle adds an explicit category for cultural and arts journalism,
which had been folded into the broader civic reporting category in
prior cycles.

## 4. Stakeholder consultation: implement the revised protocol in
   full

The revised stakeholder consultation protocol adopted in May 2025
will be fully implemented across all grantmaking decisions in 2026.
The protocol establishes when and how the foundation communicates
with donors and the public about decisions that may attract
controversy, while explicitly preserving program decisions as the
sole responsibility of staff and board.

## What we will not do

- We will not adopt content-screening criteria for grantee programs.
  Editorial judgment on book selection, journalism topics, or
  performance programming is and will remain the responsibility of
  grantees, not of the foundation.
- We will not condition grants on grantees' public stances on
  contested cultural-policy questions. Grantees who disagree with
  the foundation publicly remain eligible for renewed funding on
  the merits of their work.
- We will not enter the political-advocacy space. The foundation is
  a 501(c)(3) and operates strictly within the limits of that
  status; it does not engage in partisan or electoral activity.

---

Approved by the Board of Trustees, December 11, 2025.
""",

"past_media_partnerships.md": f"""\
# Media Partnerships — Powell's Community Foundation

{_DISCLOSURE}

The foundation works with media partners primarily through its
local journalism support program, which provides pass-through
grants to independent Oregon news organizations for civic and
cultural reporting. Listed below are the largest partnerships from
the 2024–2025 cycles, all of which preserved full editorial
independence at the recipient organization.

## Oregon Humanities Magazine — Annual Cultural-Journalism Grant

A $90,000 annual grant supporting Oregon Humanities' long-form
cultural journalism work, including its essay series on Oregon's
literary history and its profiles of regional independent
publishers. Renewed in 2025 for a third consecutive year. Editorial
control sits entirely with Oregon Humanities; the foundation has no
involvement in topic selection or editing.

## OPB — K–12 Education Reporting Project

A two-year, $180,000 commitment funding two reporting positions on
Oregon Public Broadcasting's education desk, with a focus on
Oregon's K–12 literacy outcomes and school library access. The
positions are administered entirely by OPB's editorial leadership.
The foundation does not receive review of stories produced under
the grant. OPB has published multiple stories during the grant
period that examine the foundation's own programming critically,
which the foundation has accepted as appropriate.

## Literary Arts — Wordstock Festival Sponsoring Partnership

A multi-year sponsoring partnership with the Wordstock literary
festival, $45,000 annually. The partnership covers the festival's
school-program component, which brings Title I students to author
events. The partnership is brand presence — not journalism.

## The Oregonian — Cultural Affairs Reporting Position

A 2024 one-year grant of $120,000 funding a half-time cultural
affairs reporting position at The Oregonian, with the brief to
cover regional independent publishing. The grant was not renewed
for 2025 — not for editorial reasons, but because The Oregonian's
editorial leadership concluded that the half-time structure was not
producing the depth of coverage either party had envisioned. The
foundation supported this decision and reallocated the funding to
the small-press sustainability fund.

## Decisions to decline

The foundation has declined to fund three media partnerships in the
2024–2025 cycles for failing to meet its editorial-independence
requirements: cases where the proposed structure would have given
the foundation review rights over content, or where the topical
brief was so narrow that the funded position could not have
operated independently of the funder's interests. The foundation's
written grant terms specify that any such conditions are
disqualifying.
""",

"press_releases/2024-10-08-2025-grants-cycle.md": f"""\
# Powell's Community Foundation announces 2025 grants cycle, expands literacy and small-press programs

*Portland, Oregon — October 8, 2024.* Powell's Community Foundation
announced today that its 2025 grants cycle will distribute $14.4
million across four program areas, with substantial expansions in
the foundation's K–12 literacy and independent publishing programs.

"This cycle reflects two years of listening to grantees about what
they need most," said Margaret Hsu, the foundation's Executive
Director, in remarks at the foundation's annual stakeholder meeting
held at the Old Library at Lewis & Clark College. "What we heard
consistently was that operating support — the kind of support that
keeps the lights on, not the kind that funds a specific project —
is the form of grant that small presses and small literary magazines
need most and receive least. The 2025 cycle responds to that."

The 2025 grant allocations are:

- **K–12 literacy programs**: $5.6 million, an increase of 18% from
  2024, including $2.4 million for the School Librarian Fund.
- **Independent publishing**: $3.8 million, including the new
  Pacific Northwest small-press sustainability fund.
- **Local journalism support**: $2.6 million in pass-through grants
  to Oregon and Washington news organizations.
- **Library access**: $2.4 million to support branch operations and
  bilingual programming at Multnomah County Library and partner
  systems.

The foundation also announced that it will open applications for
the 2025 local journalism program on January 8, 2025, with awards
announced in April. The 2025 cycle includes a new category for
cultural and arts journalism, in addition to the existing civic
reporting category.

Application materials and program guidelines are available at
powellscf.org/2025-grants. The foundation will host two information
sessions for prospective applicants — one at the Hollywood Branch
Library on November 6 and one virtually on November 14.

*Press contact: Anjali Mehta, Chief Financial Officer,
press@powellscf.org, (503) 555-0188.*
""",

"press_releases/2025-05-13-school-librarian-fund.md": f"""\
# Powell's Community Foundation expands School Librarian Fund to 18 Title I schools

*Portland, Oregon — May 13, 2025.* Powell's Community Foundation
announced today that its School Librarian Fund — which provides
direct salary support for librarian positions in Title I schools
that have lost librarian funding through district budget cuts —
will expand from 12 funded positions in the 2024–25 academic year
to 18 funded positions in the 2025–26 academic year.

The expansion adds librarian positions in three David Douglas
schools and three schools in the Reynolds school district. Each
position is funded at full FTE under a renewable three-year
commitment, with the foundation covering 100% of salary and
benefits.

"The students at these schools were losing access to a librarian
not because the work was unimportant, but because the funding
arrangement was unsustainable," said Jonathan Forsythe, the
foundation's Director of Programs, at a press event held at Lent
K–8 in Southeast Portland. "What we're doing is putting that
funding back, openly, with the understanding that this is a
medium-term commitment."

The expansion comes as several Oregon school districts continue to
report librarian-position cuts driven by general-fund pressures.
The foundation's analysis, conducted in partnership with the
Oregon Library Association, identified 31 Title I schools in the
Portland metro area as priority candidates for librarian funding
support. The 18 funded positions cover 58% of those schools.

The foundation will host an open house at Lent K–8 on May 21 to
share details of the program with school administrators in
neighboring districts. The foundation does not anticipate further
expansion of the program in 2026 but will reassess the funding
landscape annually.

*Press contact: Anjali Mehta, Chief Financial Officer,
press@powellscf.org.*
""",

"press_releases/2025-11-04-board-statement-reading-list.md": f"""\
# Powell's Community Foundation board reaffirms commitment to grantee editorial independence

*Portland, Oregon — November 4, 2025.* The board of trustees of
Powell's Community Foundation issued a statement today reaffirming
its policy of full grantee editorial independence, in response to
sustained criticism from a small organized group, Parents First
Oregon, regarding a foundation-funded K–12 reading list.

The board's review process — which extended over 90 days and
included public comment, written submissions from Parents First
Oregon, and consultation with educators — concluded with a March
2025 decision to maintain the original reading list without
changes. Today's statement, prompted by renewed pressure on the
foundation in October, restates that decision and clarifies the
foundation's policy framework.

"Reading lists curated by educators are educator decisions," said
Margaret Hsu, the foundation's Executive Director, in remarks
delivered alongside the board statement. "The foundation's role is
to fund, not to curate. The board has restated this policy clearly
because clarity matters in this moment, and because the alternative
— a foundation that adjusts its grantmaking under organized public
pressure — would compromise our work and the work of every grantee
we support."

The statement notes that the foundation continues to fund all three
of the contested titles in subsequent grant cycles, and that the
foundation's grant terms explicitly specify that any conditioning
of grants on stance taking would be disqualifying for the
foundation as a 501(c)(3).

The board also acknowledged criticism from a separate direction —
that the foundation had not consulted long-time donors adequately
during the March review process. The foundation's revised
stakeholder consultation protocol, adopted in May 2025, addresses
this by clarifying when and how donors will be informed about
controversies. The protocol does not give donors any role in
program decisions.

The full board statement is available at powellscf.org/board-statements.

*Press contact: Anjali Mehta, Chief Financial Officer,
press@powellscf.org.*
""",

"press_releases/2026-03-12-journalism-fund-2026.md": f"""\
# Powell's Community Foundation opens 2026 local journalism support cycle

*Portland, Oregon — March 12, 2026.* Powell's Community Foundation
opened applications today for its 2026 local journalism support
program, with $2.8 million committed for distribution across
independent Oregon news organizations.

The 2026 cycle accepts applications across two categories: civic
reporting (covering city, county, and state government, public
agencies, and ballot measures) and cultural and arts journalism
(covering literature, music, theater, visual arts, and food and
drink in Oregon). Grants will range from $25,000 to $90,000, with
larger awards available for multi-year commitments at
$150,000–$220,000 over three years.

"The journalism program operates as pass-through funding," said
Margaret Hsu, the foundation's Executive Director. "The foundation
provides the financial commitment. The recipient organization
maintains full editorial control over how the money is used. We do
not review story selection, editing, or publication decisions, and
we do not receive advance copies of work."

Eligible applicants are independent news organizations, defined as
501(c)(3) nonprofits or for-profit organizations operating under a
written editorial-independence policy that the foundation can
review during application processing. Single-publisher newsletters
are eligible if they meet the editorial-independence requirements.

Applications are due May 15, 2026. Awards will be announced in
July. Application materials and the foundation's grant terms are
available at powellscf.org/2026-journalism-grants.

The foundation will host two information sessions for prospective
applicants: one at Powell's City of Books on April 9, and one
virtually on April 16.

*Press contact: Anjali Mehta, Chief Financial Officer,
press@powellscf.org.*
""",
}


# ---- Cascadia Credit Union --------------------------------------------------

_CASCADIA_CU: dict[str, str] = {
"profile.md": f"""\
# Cascadia Credit Union

{_DISCLOSURE}

Cascadia Credit Union is a member-owned cooperative financial
institution serving approximately 152,000 members across Oregon and
Southwest Washington. Cascadia operates 22 full-service branches
across the Portland metro area, the Willamette Valley, and Southwest
Washington (Vancouver, Camas, Battle Ground), and a digital-only
service tier available throughout its community charter area.

The credit union was founded in 1964 as the Portland Public Schools
Federal Credit Union, serving teachers and school staff. In 2002 it
expanded to a community charter and adopted its current name. As of
year-end 2025, Cascadia held $4.2 billion in assets and reported
2025 net income of $48 million, distributed to members through
patronage rebates, branch reinvestment, and contributions to its
Community Reinvestment Fund.

## Products

- **Sustainable Mortgage**: a mortgage product with a 0.25% rate
  reduction for homes meeting Energy Trust of Oregon residential
  efficiency standards.
- **First-Time Homebuyer Bridge**: down-payment assistance up to
  $20,000 for first-time homebuyers in eligible Oregon and
  Washington census tracts, structured as a forgivable second
  position loan.
- **EV Auto Loans**: rate reductions of 50–100 basis points on auto
  loans for eligible electric vehicles, including new and qualified
  used vehicles.
- **Sustainability Savings**: a money-market product with rates
  pegged to the credit union's overall lending in
  efficiency-aligned categories.

## Leadership

- **Eric Carlsen**, President and CEO since 2019. Previously CEO of
  Iowa Community Credit Union; before that, regional president at
  USAA Federal Savings Bank. Holds an MBA from the University of
  Iowa.
- **Maria Lopez**, Chief Marketing Officer. Joined Cascadia in 2022.
  Previously VP for member experience at Patelco Credit Union in
  Northern California.
- **Robert Yu**, Chief Lending Officer. Twenty-six years at Cascadia
  in progressively senior lending roles.

The credit union is governed by a nine-member volunteer Board of
Directors elected by the membership. Three board seats are up for
election each year on rotating three-year terms.

## Position on contested issues

In June 2025 the National Credit Union Administration's
Pacific-region examiners issued a Document of Resolution (DOR)
following the credit union's annual examination, citing supervisory
concerns about Cascadia's third-party fintech partnership for
digital member onboarding. The DOR identified three specific
findings: insufficient documentation of the fintech partner's
identity-verification controls, gaps in periodic recertification of
member identity records, and inadequate board reporting cadence on
fintech-partner risk metrics.

Cascadia accepted the findings without contesting them and
submitted a corrective action plan within the regulatory window. As
of February 2026 the credit union has completed two of the three
required remediations, with the third (board reporting cadence
revisions) on track for completion by April 30, 2026.

CEO Eric Carlsen, in a December 2025 letter to members published on
the credit union's website, framed the credit union's position
plainly: "We took a calculated bet on a fintech partnership that
moved faster than our internal controls could supervise. The
examiners were right to flag it. We're fixing it on the timeline we
committed to, and we're publishing our progress in writing because
that's what members deserve."

The credit union has opted not to renew the disputed fintech
partnership for 2026. The replacement provider was selected through
a competitive process that included direct review by the board's
audit committee.

On lending: Cascadia's Sustainable Mortgage product has been
publicly criticized by some members and by housing advocacy
organizations as accessible primarily to higher-income members who
can afford the certification costs of an Energy Trust–rated home.
The credit union has acknowledged the critique and committed to
publishing borrower-income distribution data for the program
beginning Q3 2026.
""",

"brand_priorities_2026.md": f"""\
# 2026 Member Communication Priorities — Cascadia Credit Union

{_DISCLOSURE}

_Approved by the Cascadia Credit Union Marketing and Member
Experience Committee, January 2026._

Cascadia's 2026 member-communication priorities were shaped by two
inputs: the December 2025 member survey (49% response rate from a
random sample of 8,000 members) and the strategic plan adopted by
the board in November 2024.

## 1. Financial literacy programming for under-35 members

Cascadia's under-35 membership is growing fastest, but our member
survey found that this group reports the lowest satisfaction with
the credit union's educational content. The 2026 priority: a
quarterly financial-literacy content series specifically designed
for under-35 members, distributed across newsletters, branches,
social, and partner outlets.

The series will cover four topic clusters tied directly to
under-35-member life events: (a) renting in a tight Portland market,
(b) saving for a first home down payment, (c) student loan
refinancing post-2025 federal-loan changes, and (d) credit-building
when starting from zero. Topics chosen by member survey priority,
not internal hypothesis.

Distribution partners under consideration: The Cascade Tribune,
Willamette Week, and OPB. Final selection contingent on each
partner's editorial-firewall posture.

## 2. Honest communication about the NCUA Document of Resolution

The 2025 NCUA examination is closed; the corrective action plan
remains open. We will continue to publish remediation progress
quarterly through 2026, even after the DOR is formally resolved by
the regulator, because members have asked us to. This is not a
crisis-communications issue. It's a standing commitment to operate
transparently around supervisory matters.

## 3. Sustainable Mortgage transparency

Cascadia will publish borrower-income distribution data for the
Sustainable Mortgage program in Q3 2026, alongside the broader
mortgage book for context. We've heard from members and housing
advocates that the program's structure favors higher-income
borrowers. The 2026 review will assess whether changes are warranted.

If the data shows the critique is correct, we will redesign the
program to broaden accessibility — including by absorbing more of
the Energy Trust certification cost into the credit union's
underwriting rather than passing it to the borrower.

## 4. First-Time Homebuyer Bridge expansion

The First-Time Homebuyer Bridge program has supported 814 first-time
buyers since launch in 2022. The 2026 expansion adds Clark County
(WA), Yamhill County (OR), and Marion County (OR) to the program's
eligible service area, doubling the program's geographic footprint.

Funding for the expansion comes from the credit union's Community
Reinvestment Fund, which is replenished annually from net income.

## What we will not do

- We will not run brand campaigns that emphasize Cascadia's
  cooperative-ownership structure as a virtue without specifying
  what the structure actually delivers to members. The cooperative
  difference has to show up in concrete member outcomes.
- We will not pursue a national expansion. Cascadia's community
  charter is Oregon and Southwest Washington. We are a regional
  institution by design.
- We will not enter the cryptocurrency or buy-now-pay-later product
  spaces in 2026. Both have been evaluated and declined by the
  product committee.

---

Approved by the Marketing and Member Experience Committee,
January 22, 2026.
""",

"past_media_partnerships.md": f"""\
# Media Partnerships — Cascadia Credit Union

{_DISCLOSURE}

Cascadia partners with media organizations primarily on financial
literacy content for under-35 members and on first-time homebuyer
education content for the regional market. The credit union does
not buy programmatic display advertising. Listed below are
partnerships from the last 18 months.

## Willamette Week — Financial Literacy Series

A six-month sponsored content series in 2025 covering topics
identified by Cascadia's member survey: renting in tight markets,
saving for a first home, building credit from zero. Six original
articles produced by Willamette Week's editorial team with
financial information provided by Cascadia and reviewed for
factual accuracy only — Willamette Week retained complete editorial
control over framing, narrative, and headline selection.

What worked: the topical focus was tight enough that editorial and
sponsor interests were aligned without conflict. The series produced
a measurable lift in under-35 member acquisition through
partner-attributed referrals.

Total budget: $48,000.

## OPB — Marketplace Sponsorship

Annual underwriting sponsorship of OPB's Marketplace broadcast
since 2023. This is brand presence — not editorial content. OPB
acknowledges Cascadia in standardized pre-program announcements.
Renewed for 2026.

Annual commitment: $32,000.

## Portland Tribune — First-Time Homebuyer Series

A 2024 four-week sponsored section that ran in spring 2024 covering
the regional first-time homebuyer landscape. Editorial control sat
with the Portland Tribune. The series produced 188 leads to
Cascadia's First-Time Homebuyer Bridge program, of which 47
converted to active applications.

The section was not renewed for 2025 because both teams concluded
that the format had reached its natural saturation in the
metro-Portland audience. The credit union reallocated the funding
to the under-35 financial literacy series.

Four-week budget: $24,000.

## Pickathon — Festival Co-Sponsor

Cascadia co-sponsored Pickathon's general operating fund in 2024
and 2025, with brand presence at the festival's main stage. The
sponsorship is not editorial content — it is regional brand
visibility. Renewed for 2026.

Annual commitment: $18,000.

## Decisions to decline

Cascadia has declined four media partnership proposals in the
2024–2025 period for editorial-firewall reasons or for topical fit
mismatches. The credit union does not enter sponsorship arrangements
where the proposed scope would touch member-facing rate or product
disclosures, because such disclosures are regulated content and
cannot sit in sponsored journalism.
""",

"press_releases/2024-12-04-annual-meeting-recap.md": f"""\
# Cascadia Credit Union holds 2024 Annual Member Meeting; reports $42M net income, expands community reinvestment

*Portland, Oregon — December 4, 2024.* Cascadia Credit Union held
its 2024 Annual Member Meeting on Tuesday at the Tualatin Hills
Recreation Center, with approximately 380 members in attendance and
2,400 additional members participating via livestream. The meeting
reported the credit union's 2024 financial results and elected
three members to the Board of Directors.

Cascadia reported 2024 net income of $42 million on assets of $4.0
billion, a 9.6% return on assets that places the credit union among
the stronger-performing institutions in its peer group. Membership
grew by 7.4% during 2024 to 148,000 members.

"This was a year where we leaned harder into community reinvestment
than we have at any point in the credit union's recent history,"
said Eric Carlsen, President and CEO, in remarks at the meeting.
"The Board's decision to expand the Community Reinvestment Fund's
share of net income from 8% to 12% was the right call, and we'll
continue at that level in 2025."

The credit union announced that the Community Reinvestment Fund
will distribute $5.0 million in 2025 across four funding categories:
financial-literacy programming, first-time homebuyer down-payment
assistance, small-business lending in underserved Oregon census
tracts, and grants to Oregon and Southwest Washington community
nonprofits.

Three Board of Directors seats were on the ballot. Two incumbents
were re-elected: Patricia Worthington and James Henry. The third
seat was won by newcomer Sarah Briggs, a Hillsboro-based small-
business owner who ran on a platform of expanded under-35 member
outreach. Briggs received 64% of the vote in a contested
three-candidate race.

The credit union also announced that its First-Time Homebuyer
Bridge program will expand into Clark County, Washington beginning
February 2025, with full availability across the credit union's
Southwest Washington branches by April.

The full meeting recording, the 2024 annual report, and the credit
union's 2024 financials are available at cascadiacu.org/2024-annual.

*Press contact: Maria Lopez, Chief Marketing Officer,
press@cascadiacu.org, (503) 555-0220.*
""",

"press_releases/2025-06-17-sustainable-mortgage-expansion.md": f"""\
# Cascadia Credit Union expands Sustainable Mortgage program to Eugene and Bend

*Portland, Oregon — June 17, 2025.* Cascadia Credit Union announced
today that its Sustainable Mortgage product — a mortgage with a
0.25% rate reduction for homes meeting Energy Trust of Oregon
residential efficiency standards — will expand to the Eugene and
Bend metropolitan areas beginning August 1.

The expansion adds two regional markets to the program, which
launched in 2023 in the Portland metro area and was extended to
Salem and the Willamette Valley in 2024. The Sustainable Mortgage
has originated approximately $186 million across 412 mortgages
since launch.

"The program has worked for the borrowers it has reached, but the
geographic footprint has been narrower than we want," said Robert
Yu, Cascadia's Chief Lending Officer, at a press event held at the
credit union's Beaverton branch. "Adding Eugene and Bend
acknowledges that energy-efficient construction is happening across
the state, not only in metro Portland, and that the program should
follow."

The expansion comes alongside acknowledgment from Cascadia
leadership of public criticism of the program. Some members and
housing advocacy organizations have argued that the Sustainable
Mortgage is most accessible to higher-income borrowers who can
afford the certification costs of an Energy Trust–rated home.

"That critique is fair, and we've heard it directly from members,"
Yu said. "The expansion to Eugene and Bend doesn't address the
income-distribution question. We're committing to publish borrower
income data for the program in 2026, and if the data confirms the
critique, we'll redesign the program."

Cascadia indicated that program redesign options under consideration
include absorbing the Energy Trust certification cost into the
credit union's underwriting rather than passing it to the borrower,
and offering an additional rate-reduction tier for borrowers below
80% of area median income.

Eligibility details and application materials for the expanded
program are available at cascadiacu.org/sustainable-mortgage.

*Press contact: Maria Lopez, Chief Marketing Officer,
press@cascadiacu.org.*
""",

"press_releases/2025-09-30-ncua-corrective-action.md": f"""\
# Cascadia Credit Union submits NCUA corrective action plan, publishes progress publicly

*Portland, Oregon — September 30, 2025.* Cascadia Credit Union has
submitted its corrective action plan in response to the National
Credit Union Administration's June 2025 Document of Resolution and
will publish quarterly progress reports through resolution and
beyond, the credit union announced today.

The Document of Resolution, issued after the credit union's annual
NCUA examination, identified three findings related to Cascadia's
third-party fintech partnership for digital member onboarding:
insufficient documentation of the fintech partner's identity-
verification controls, gaps in periodic recertification of member
identity records, and inadequate board reporting cadence on
fintech-partner risk metrics.

"We accept the findings as written," said Eric Carlsen, President
and CEO, in a member letter published alongside today's
announcement. "These are not findings we're contesting. We took a
calculated bet on a fintech partnership that moved faster than our
internal controls could supervise. The examiners were right to
flag it. We're publishing our progress in writing because that's
what members deserve."

The corrective action plan, submitted September 22, includes:

- Comprehensive documentation review of the fintech partner's
  identity-verification controls, with completion target October 31, 2025.
- Recertification of all member identity records onboarded through
  the fintech partner since 2022, with a target of January 31, 2026.
- Restructured board reporting on fintech-partner risk metrics,
  effective the Q1 2026 board meeting cycle.

The credit union also announced that it will not renew the disputed
fintech partnership for 2026. A replacement provider has been
selected through a competitive process that included direct review
by the credit union's audit committee.

Cascadia will publish progress reports on cascadiacu.org/ncua-update
on a quarterly cadence through 2026, including after the formal
resolution of the matter by NCUA. The credit union will continue
publishing the reports voluntarily because members have specifically
asked for ongoing transparency.

The full member letter and the corrective action plan summary are
available at cascadiacu.org/ncua-update.

*Press contact: Maria Lopez, Chief Marketing Officer,
press@cascadiacu.org.*
""",

"press_releases/2026-02-25-financial-literacy-series.md": f"""\
# Cascadia Credit Union launches Under-35 Financial Literacy Series with Oregon media partners

*Portland, Oregon — February 25, 2026.* Cascadia Credit Union
launched its 2026 Under-35 Financial Literacy Series today, a
quarterly content program produced in partnership with three
Oregon media organizations and designed to address the financial
information needs identified in the credit union's December 2025
member survey.

The series will run across four topic clusters tied directly to
under-35-member life events: renting in a tight Portland market,
saving for a first home down payment, student loan refinancing
following the federal Department of Education's 2025 program
changes, and credit-building from zero.

"The series exists because our under-35 members told us, clearly,
that we weren't producing useful educational content for them,"
said Maria Lopez, Cascadia's Chief Marketing Officer, at the
program's launch event held at the Pearl District branch. "Topics
were chosen by member survey priority, not by internal hypothesis."

Media partners for the series include The Cascade Tribune, OPB
Marketplace, and KGW's Sunrise Money segment. Each partner produces
content under its own editorial direction; Cascadia's role is
limited to providing the funding commitment and to fact-checking
financial information for accuracy.

"We do not have story-selection input or editorial review rights,"
Lopez said. "If a partner produces content critical of credit unions
generally or of Cascadia specifically, that's appropriate. The
series is meant to serve the audience, not the credit union's brand."

The series begins with the rental-market topic in March, with
content publishing across the partners' channels through April. The
remaining three topics will run quarterly through the end of 2026.
All series content will be republished without paywall or partner-
specific gating on cascadiacu.org/under-35.

*Press contact: Maria Lopez, Chief Marketing Officer,
press@cascadiacu.org.*
""",
}


# ---- Stumptown Roasters Co-op -----------------------------------------------

_STUMPTOWN: dict[str, str] = {
"profile.md": f"""\
# Stumptown Roasters Co-op

{_DISCLOSURE}

Stumptown Roasters Co-op is a worker-owned cooperative specialty
coffee roaster headquartered in Portland, Oregon, with retail cafés
in four neighborhoods (Downtown, Hawthorne, Foster-Powell, North
Mississippi) and wholesale distribution across the West Coast and
selected national specialty markets. The roastery is located in
Foster-Powell.

The company was founded as a privately held specialty roaster in
1999 and grew through the 2000s and 2010s as part of the third-wave
specialty coffee movement. In 2022 the company converted to a
worker-owned cooperative structure following a buyout led by
long-tenure employees and supported by Project Equity and the
Northwest Cooperative Development Center. As of February 2026 the
co-op has 280 worker-owners across all roles.

## Operations

- **Retail cafés**: four full-service Portland locations plus a
  small kiosk operation at Portland International Airport.
- **Roastery**: a 21,000-square-foot facility in Foster-Powell
  producing approximately 980,000 pounds of roasted coffee
  annually. The facility includes a public cupping space available
  for community programming.
- **Wholesale**: distribution to approximately 320 cafés,
  restaurants, hotels, and grocery accounts across Oregon,
  Washington, California, New York, and Massachusetts.
- **Direct-trade sourcing**: green coffee purchased through direct
  relationships with farmers and farmer cooperatives in Ethiopia,
  Burundi, Honduras, Peru, Colombia, and Indonesia.

## Leadership

Cooperative governance: a member-elected General Manager and a
seven-seat Worker Council elected to staggered two-year terms by
the worker-owner membership. Operational leadership reports to the
General Manager; strategic decisions above a defined threshold
require Council approval.

- **Allison Tate**, General Manager since the cooperative
  conversion in 2022. Joined the company in 2014 as a barista;
  served as Café Operations Director 2018–2022.
- **Hugo Tomlinson**, Roasting Director. Twelve-year tenure with
  the company; SCA Q-Grader certified.
- **Ines Castellanos**, Sourcing Director. Joined in 2019 from
  Counter Culture Coffee in Durham, North Carolina.

## Direct trade and origin programs

Stumptown maintains direct relationships with 41 farmer
cooperatives and individual producers across six origin countries.
Sourcing prices average 28% above the C-market reference price
for the relevant grade and origin. The company publishes its annual
green coffee transparency report at stumptownroasters-coop.com/transparency.

## Position on contested issues

In autumn 2024, café workers at four Stumptown wholesale partner
cafés in California — owned and operated by separate businesses
that purchase Stumptown coffee — initiated a unionization campaign
under the Service Employees International Union. The campaigns
became the subject of national specialty-coffee press coverage,
including coverage in Sprudge and Eater.

Stumptown's leadership response: the cooperative is not the
employer of record at the wholesale partner cafés and has no
authority over labor decisions there. The cooperative does not
weigh in publicly on labor questions at independently owned
businesses that purchase Stumptown coffee, regardless of whether
those decisions favor or disfavor unionization.

For the cooperative's own workforce, the cooperative model
addresses the underlying questions that drive unionization
campaigns elsewhere — wages, scheduling, benefits, voice in
operational decisions — through structural worker ownership and
the Worker Council governance model, rather than through a
collective bargaining relationship with management. The
cooperative's worker-owners have chosen this structure
democratically through the 2022 conversion vote (94% in favor) and
again through three subsequent annual member meetings.

The cooperative has stated publicly that if its worker-owners
voted to also organize collectively under a union, the cooperative
would respect that outcome. There is no current campaign at any
cooperative-owned location.

In December 2024 the cooperative published a position document
clarifying the above on its website, in response to questions from
trade press. The document remains the cooperative's standing
public position.
""",

"brand_priorities_2026.md": f"""\
# 2026 Brand Priorities — Stumptown Roasters Co-op

{_DISCLOSURE}

_Approved by the Worker Council, January 2026._

The cooperative's 2026 brand priorities reflect the operational
realities of a worker-owned business at our scale: we have a
strong national specialty positioning, a regional retail footprint
in Portland that runs hot, and a wholesale book that has grown 11%
year-over-year for three consecutive years. The 2026 priorities
focus on consolidating these strengths rather than reaching for
new territory.

## 1. Origin storytelling — direct trade transparency reports

The cooperative will publish its 2025 green coffee transparency
report in March 2026, with expanded detail on producer-level
pricing, multi-year purchase commitments, and pre-financing
provided to producer cooperatives. The 2025 report covers all 41
direct-trade relationships and will be the most detailed origin-
program disclosure the company has published.

A six-part editorial series accompanying the report — covering
specific producer cooperatives in Yirgacheffe, Burundi, and the
Cauca region of Colombia — will run in our owned channels
(newsletter, blog, in-café) and we'll explore co-publishing with
Plate & Place at The Cascade Tribune.

## 2. Worker-ownership model — clear, specific communication

A common pattern in our member feedback: customers and trade press
are interested in the cooperative model but find our existing
explanations vague. The 2026 priority is producing clear, specific
content about what the cooperative model means for daily decisions
— what the Worker Council does, how pricing decisions get made,
how new café locations get approved. This is education, not brand-
building.

## 3. Regional retail footprint — operational consolidation

The cooperative is not opening new Portland café locations in
2026. The 2025 fiscal year confirmed that our four existing café
locations are operating below capacity through significant portions
of the day; the operational priority is improving those locations
before adding new ones. New locations remain on the long-range
plan but are deferred to 2027 at earliest.

## 4. Wholesale specialty — sustainable growth, not aggressive expansion

The wholesale book added 18 new accounts in 2025. The 2026 target
is 12–18 new accounts, with explicit preference for accounts that
are themselves operating sustainably (single-location or
small-chain specialty cafés, restaurants with strong specialty-
coffee programs, hotels with established food-and-beverage
identities). The cooperative will not pursue aggressive wholesale
expansion that would require capacity additions at the roastery in
2026 or 2027.

## 5. National brand presence — Plate & Place territory only

For 2026 sponsored content and brand programs, the cooperative
will work with media partners whose audience includes a meaningful
West Coast specialty-coffee or food-and-drink subset. The Cascade
Tribune's Plate & Place newsletter is a partner under active
consideration. National-scale partnerships outside this audience
profile will be deferred.

## What we will not do

- We will not pursue private equity investment, brand licensing
  arrangements, or any structure that would alter the cooperative
  ownership model.
- We will not enter the ready-to-drink canned coffee category in
  2026. The category has been evaluated by the Worker Council and
  declined for 2026.
- We will not run brand campaigns about the cooperative model that
  imply moral superiority over non-cooperative coffee businesses.
  The cooperative is one structure among several; we present it as
  ours, not as the right answer for everyone.

---

Approved by the Worker Council, January 18, 2026.
""",

"past_media_partnerships.md": f"""\
# Media Partnerships — Stumptown Roasters Co-op

{_DISCLOSURE}

The cooperative works with media organizations primarily on origin
storytelling and on coverage of the worker-ownership model.
Listed below are partnerships from the last 18 months.

## Eater Portland — Origin Producer Profile Series

A 2025 four-part profile series in Eater Portland covering
specific direct-trade producer relationships: a women-led
cooperative in Yirgacheffe, a youth-led producer association in
Burundi, the Cauca-region cooperative the company sources its
flagship Colombian coffee from, and a fourth-generation producer
in Antigua, Guatemala.

Editorial control sat with Eater Portland. The cooperative
provided producer access (with producer consent), green coffee
pricing data, and travel funding for the writer. The series ran
from May through August 2025.

What worked: the format suited Eater Portland's audience and the
specificity of the producer relationships. Three of the four
profiles were syndicated by national specialty-coffee outlets,
extending reach without additional spend.

Total budget: $32,000 (covering writer travel, producer-side
hospitality, photography licensing).

## PDX Magazine — Cooperative Conversion Anniversary Feature

A standalone feature in PDX Magazine's August 2024 issue covering
the cooperative's two-year anniversary of the worker-ownership
conversion. PDX Magazine's editorial team interviewed worker-
owners across roles and produced an unsparing profile that
included both successes (worker retention, wage progression) and
challenges (the ongoing operational complexity of cooperative
governance).

The cooperative did not provide financial support for the feature.
The relationship was access-only.

## Sprudge — Conversation Series

The cooperative co-funded Sprudge's three-part 2024 conversation
series on cooperative ownership in specialty coffee, covering
case studies from the United States, Italy, and Argentina. The
cooperative was one of five funders. Editorial control sat with
Sprudge.

Funding contribution: $8,000.

## OPB — Marketplace Underwriting

Annual underwriting sponsorship of OPB Marketplace's regional
broadcast since 2023. Brand presence; no editorial content.
Renewed for 2026.

Annual commitment: $14,000.

## Decisions to decline

The cooperative has declined three media partnership proposals in
2024–2025 that would have required positioning the cooperative
ownership model as superior to non-cooperative specialty coffee
businesses. The cooperative does not pursue brand campaigns that
diminish other operating models in the specialty industry.

The cooperative has also declined to participate in two
documentary projects that proposed coverage of the labor-
unionization dynamics at independently owned wholesale partner
cafés. The cooperative does not weigh in publicly on labor
decisions at independently owned businesses that purchase its
coffee.
""",

"press_releases/2024-11-19-coop-anniversary-report.md": f"""\
# Stumptown Roasters Co-op publishes second-year report on worker-ownership conversion

*Portland, Oregon — November 19, 2024.* Stumptown Roasters Co-op
published its second-year report today on the cooperative's 2022
conversion to worker ownership, covering operating results,
worker-ownership economics, and ongoing operational challenges of
the cooperative governance model.

The report, audited for accuracy by the Northwest Cooperative
Development Center, is available without paywall at
stumptownroasters-coop.com/year-two-report.

"The report exists because we said in 2022 we would publish one,
and because the cooperative ownership model only works to the
extent it is honest about how it's operating," said Allison Tate,
General Manager, in remarks at the report's release event held at
the cooperative's Foster-Powell roastery.

Findings reported include:

- The cooperative reached 280 worker-owners by year-end 2024, up
  from 248 at the time of conversion. Twelve worker-owners have
  exited the cooperative since conversion; their equity shares were
  redeemed under the cooperative's standard exit terms.
- Worker-owner average compensation (wages plus distributed surplus)
  reached $58,400 in 2024, a 14% increase from the pre-conversion
  baseline of $51,200 (in 2024 dollars).
- Worker retention measured at 89% on a one-year basis, compared
  with industry benchmark retention rates of approximately 62% at
  similar-scale specialty coffee operations.
- The cooperative's wholesale revenue grew 11% in 2024; café
  revenue grew 4%.

The report also identifies operational challenges. Cooperative
governance produces longer decision cycles than the company's
prior structure: three operational decisions in 2024 (a wholesale
account expansion, a roastery shift schedule change, and a wage
band revision) took 6–11 weeks to resolve through the Worker
Council process where the prior structure would have resolved them
in 1–2 weeks. The Worker Council reviewed governance procedures in
October 2024 and adopted a revised threshold framework for
operational versus strategic decisions.

"The slower decision-making is not always a cost," Tate said. "Some
of the decisions that took longer in 2024 turned out to be better
decisions because of the longer cycle. That's not always the case,
and we're working on the cases where it isn't."

The cooperative will continue publishing the year-end report
annually for the foreseeable future.

*Press contact: contact@stumptownroasters-coop.com.*
""",

"press_releases/2025-04-08-burundi-direct-trade.md": f"""\
# Stumptown Roasters Co-op expands direct-trade program to second Burundi cooperative

*Portland, Oregon — April 8, 2025.* Stumptown Roasters Co-op
announced today that its direct-trade green coffee program will
add a second producer cooperative in Burundi to its sourcing
relationships, beginning with the 2025 fly-crop harvest.

The new partner is the Mukoni Cooperative, a 940-member producer
cooperative in Kayanza Province, in northern Burundi. Mukoni joins
the cooperative's existing relationship with the Mubuga Producer
Association, which has been a Stumptown direct-trade partner since
2017.

"Burundi has been an important origin for the cooperative for
nearly a decade," said Ines Castellanos, Sourcing Director, in
remarks at a public cupping event held at the Foster-Powell
roastery. "Adding a second producer relationship gives us a
fuller picture of what the country can offer in different growing
conditions, and gives Mukoni a U.S.-market entry under direct-trade
terms."

Sourcing pricing for Mukoni will average 31% above the C-market
reference price for the comparable washed Arabica grade. The
agreement includes pre-financing of the 2025 harvest and a
multi-year letter of intent for 2026 and 2027 purchases.

Stumptown's direct-trade transparency report, scheduled for
publication in March 2026, will include detailed pricing data for
both Burundi relationships in the 2025 reporting cycle.

The first roasted coffee from Mukoni Cooperative will be available
in Stumptown cafés and through wholesale partners beginning in
August 2025, with limited single-origin batches available through
the cooperative's website.

*Press contact: contact@stumptownroasters-coop.com.*
""",

"press_releases/2025-08-26-position-document-update.md": f"""\
# Stumptown Roasters Co-op restates standing position on labor questions at independent wholesale partner cafés

*Portland, Oregon — August 26, 2025.* Stumptown Roasters Co-op
published an updated standing-position document today on the
cooperative's role in labor questions at independently owned cafés
that purchase Stumptown coffee. The updated document restates and
clarifies the position originally published in December 2024.

The position document, available at stumptownroasters-coop.com/standing-positions,
addresses persistent questions from trade press and customers about
unionization campaigns at four California-based wholesale partner
cafés in 2024–2025. The cafés in question are owned and operated
by independent business owners; Stumptown supplies coffee to them
under wholesale agreements and is not the employer of record.

"The cooperative is not the employer of record at independently
owned wholesale partner cafés and has no authority over labor
decisions there," the document states. "We do not weigh in publicly
on labor questions at independently owned businesses that purchase
our coffee, regardless of whether those decisions favor or disfavor
unionization."

The document clarifies that the cooperative's own worker-owners —
employees of the cooperative itself — have chosen the worker-
ownership structure as their preferred form of workplace governance
through the 2022 conversion vote (94% in favor) and through three
subsequent annual member meetings. There is no current
unionization campaign at any cooperative-owned location.

The document also states that if cooperative worker-owners voted
to also organize collectively under a union, the cooperative would
respect that outcome and bargain in good faith. The cooperative
takes no position on whether such an outcome would be desirable;
the position is that the choice belongs to the worker-owners.

The updated document was approved by the Worker Council on August
20, 2025.

*Press contact: contact@stumptownroasters-coop.com.*
""",

"press_releases/2026-01-21-alberta-cafe-deferred.md": f"""\
# Stumptown Roasters Co-op confirms no new Portland café openings in 2026

*Portland, Oregon — January 21, 2026.* Stumptown Roasters Co-op
confirmed today that the cooperative will not open new Portland
café locations during 2026, deferring previously discussed
locations on Alberta Street and in Sellwood to 2027 at the earliest.

The decision was approved by the Worker Council on January 18 as
part of the 2026 strategic plan. The deferral reflects findings
from a 2025 operational review that identified meaningful
under-utilized capacity at the cooperative's four existing
Portland locations, particularly during weekday afternoon hours.

"The work for 2026 is not adding café locations," said Allison
Tate, General Manager, in a member communication accompanying
the announcement. "The work is making the four locations we
operate work harder, and that means investing in throughput,
staffing, and food program improvements rather than spreading
ourselves to new addresses."

The cooperative's 2026 operational priorities include: a phased
expansion of the food program at the Hawthorne and Foster-Powell
locations, an updated point-of-sale system that has been in
testing since November 2025, and revised staffing models for
weekday afternoons. Capital expenditure budgeted for the deferred
new locations has been reallocated to these projects and to a
delayed roastery equipment upgrade.

The Alberta Street and Sellwood locations remain in the
cooperative's long-range plan and will be reassessed in the 2027
strategic planning cycle. Lease commitments at both locations
were structured with deferral options that have now been
exercised.

The cooperative's 2026 strategic plan, including the deferral
decision, is available to worker-owners on the internal portal
and in summary form on the cooperative's website at
stumptownroasters-coop.com/2026-plan.

*Press contact: contact@stumptownroasters-coop.com.*
""",
}


# Wire up the master dict.
#
# The 4 existing sponsors get their leadership.md merged in from
# _existing_leadership.leadership (introduced in Phase 0 of Sponsor Desk —
# the prospect-brief tool's Section 3 needs a leadership.md per sponsor and
# this file did not previously exist for the original four).
#
# The 10 new sponsors come from lib/sponsors_new/<slug>.py modules added
# in Phase 0. Each module exposes a `content: dict[str, str]` of the same
# shape as the existing _PGE / _POWELLS_CF / etc. dicts.
SPONSORS: dict[str, dict[str, str]] = {
    "portland-general-energy":      {**_PGE,         "leadership.md": _existing_leadership.leadership["portland-general-energy"]},
    "powells-community-foundation": {**_POWELLS_CF,  "leadership.md": _existing_leadership.leadership["powells-community-foundation"]},
    "cascadia-credit-union":        {**_CASCADIA_CU, "leadership.md": _existing_leadership.leadership["cascadia-credit-union"]},
    "stumptown-roasters-coop":      {**_STUMPTOWN,   "leadership.md": _existing_leadership.leadership["stumptown-roasters-coop"]},
    "pacific-tower-development":    pacific_tower_development.content,
    "onpoint-cooperative":          onpoint_cooperative.content,
    "pacific-northwest-health":     pacific_northwest_health.content,
    "reed-college-press":           reed_college_press.content,
    "meyer-northwest-trust":        meyer_northwest_trust.content,
    "lewis-clark-foundation":       lewis_clark_foundation.content,
    "cascadia-outfitters-coop":     cascadia_outfitters_coop.content,
    "bull-run-cider":               bull_run_cider.content,
    "travel-oregon":                travel_oregon.content,
    "portland-museum-of-art":       portland_museum_of_art.content,
}


def write_all_sponsors(rng: random.Random, sponsors_dir: Path) -> int:
    del rng
    count = 0
    for slug in sorted(SPONSORS.keys()):
        files = SPONSORS[slug]
        base = sponsors_dir / slug
        for rel_path in sorted(files.keys()):
            content = files[rel_path]
            _check_banned(content, f"{slug}/{rel_path}")
            if "press_releases/" in rel_path and '"' not in content and "said" not in content.lower():
                raise RuntimeError(
                    f"press release {slug}/{rel_path} is missing a quoted speaker"
                )
            target = base / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            count += 1
    return count
