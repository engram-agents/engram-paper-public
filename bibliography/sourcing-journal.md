# Bibliography sourcing journal

Dated record of sourcing decisions for the paper's bibliography, moved out of `paper/bibliography.md` on 2026-09-23 so the rendered paper carries only what a reader needs; the bibliography's own extraction rule still governs entries.

***Hansson* was needed before round 2 — and then stopped being needed.** The
Condition-3 argument used to state his `Relevance` and `Core-Retainment` postulates as
met (then Ch3 §3.5, Ch4 §4.4). That claim is withdrawn: AGM/Hansson is noted for
contrast at Ch3 §3.9 and no postulate is claimed for ENGRAM, so nothing in the paper
leans on the primary any more; the philosophers can wait. **AGM has left this list entirely** — see below.

*The postulate STATEMENTS are verified*, against two documents read first-hand:
the Stanford Encyclopedia of Philosophy entry "Logic of Belief Revision" (copyright
2026 Sven Ove Hansson — the postulates' own author),
<https://plato.stanford.edu/entries/logic-belief-revision/>, and Rocha, A. C. &
Wassermann, R., "Postulates Here, Postulates Everywhere: A Discussion of Contraction
Postulates", CEUR-WS Vol-4239,
<https://ceur-ws.org/Vol-4239/paper-Rocha-11.pdf>. Both are free, and both are now
**held as well as linked** — `paper_research/source_pdfs/rocha_wassermann_postulates_ceur4239.pdf`,
which is CC BY 4.0 and therefore committed, and `.../hansson_sep_logic_belief_revision.html`,
which is copyrighted and so held on disk but **git-ignored**, exactly like the two
primaries below. A reader cloning this repository gets the first and not the second. Neither is a bibliography entry and neither is
claimed as one. The verification changed the argument rather
than confirming it. `Relevance` requires a witnessing set that contains the
contraction result and `Core-Retainment` does not, so the two are not
interchangeable; and both quantify over beliefs *upstream* of the contracted belief
— ones that help derive it — whereas the retraction cascade marks beliefs
*downstream*. Neither postulate is therefore a property the cascade has or lacks.
The resulting claim change sits with the reviewer, not in this file.

**AGM 1985 AND ALCHOURRÓN & MAKINSON 1982 ARE NOW ENTRIES ABOVE, BUILT FIRST-HAND.**
Lei located a free full text of AGM 1985 on 2026-09-21 after the not-acquiring
decision was taken, which retires that decision for this work rather than arguing
against it. Both PDFs are held at `paper_research/source_pdfs/`
(`agm_1985_partial_meet.pdf`, `alchourron_makinson_1982_theoria.pdf`), git-ignored
like the other copyrighted primaries but present on disk, so each is checkable exactly
as the Doyle, Parfit, Tulving and Nozick entries are — by holding the file, not by
cloning this repository. Entries here rest on three different footings and it is worth
saying so once: some on committed files a cloner receives, some on held-but-ignored
ones, and one — Semon — on no file at all, as its own note states. Every field in both was read off the
document — title page, final page, running heads, footer signature — with exactly two
exceptions, each noted in place rather than here: the 1982 offprint's volume number,
which it does not print at all, and its opening page number 14, which follows from the
folio sequence. The volume is omitted rather than lifted from AGM 1985's
reference list, which does print it.

***Hansson 1991* remains unacquired, and that is a decision rather than a gap.** Lei's
ruling, 2026-09-21, in his own words: *"We shouldn't rely on our memory for claims
that OTHERS make, we should always cite the sources directly."* Applied here that
rules out the tempting middle path — softening the claims and attributing them to
trained memory — and rules **in** a narrower one: state only what a held, read
document supports, and cite that document. *Studia Logica* wants ~$40 and
institutional access does not unlock it.

**The repair has LANDED, and this is what the chapters now do.** The former Ch3 §3.5
and Ch4 §4.4 asserted that the cascade *satisfies* the postulates — "ENGRAM's cascade
meets exactly these postulates"; "the cascade satisfies Hansson's belief-base
postulates". Both assertions are withdrawn. AGM/Hansson is noted for contrast at Ch3
§3.9 as the closed-theory idealisation ENGRAM is defined against, no postulate is
claimed for ENGRAM, and AGM no longer appears among the convergent traditions.
**Two consequences, and the second is why issue #58 changes rather than merely
narrowing.** The chapters now cite neither the postulate statements nor Rocha &
Wassermann — only §3.9's provenance tag names them, and that tag is a statement of what
was read rather than a citation the argument rests on (the renderer strips bare node IDs,
not the tag sentence, so the tag itself does appear in the rendered paper) — so
bullets 3 and 4 below are recorded for the record rather than describing live
citations. And **no dated Hansson work is named anywhere in the paper.** Appendix A names
"Hansson's belief-base postulates" only to point at §3.9's provenance tag and to say
the bibliography lists them without a held source document; Appendix B records
Kumiho's *self-claimed* compliance, sourced from the Kumiho paper. So #58's reversal
trigger is void — no encyclopedia citation remains to object to — **and the
acquisition it tracks is aimed at the wrong work: 1991 mattered only while the paper
stated the postulates.**

*This paragraph asserted, until 2026-09-22, that Appendix A named **Hansson 1999**.
That was true when written and stopped being true when PR #60 reworded the appendix
to name only works we hold — the same afternoon. It is corrected rather than deleted
because the stale form is the shape this file exists to catch: a sourcing record that
outlives the sentence it records, in the one file whose job is to be accurate about
sources.*

- the belief-**base** level, and the distinction from the theory level — **Alchourrón
  & Makinson 1982**, now an entry above;
- partial meet contraction and revision, and the Gärdenfors postulates in their
  original form — **AGM 1985**, now an entry above;
- the statements of `Relevance` and `Core-Retainment` — **Hansson's own Stanford
  Encyclopedia entry**, cited *as the encyclopedia entry* and never as the 1991 paper;
- that `Relevance` is strictly stronger than `Core-Retainment` — **Rocha & Wassermann**.

**What the remaining decision costs, stated rather than hidden:** we cannot establish
whether Hansson *argues* for the consistency-restoration imperative or merely
inherits it from AGM, so Ch4 defends ENGRAM's divergence against the postulate as
stated rather than against his reasoning for it.

**One descriptor is retained for a single purpose — ordering the document if the
decision is reversed.** It is read off a secondary source's reference list, so it
fails this file's extraction rule and **may not be lifted into an entry**:
**Hansson 1991**, "Belief contraction without recovery", *Studia Logica*, vol. 50,
reported as pp. 251–260 — which the secondary sources give as the postulates' primary
home rather than the 1999 Kluwer textbook these notes had been crediting. It is
marked in place rather than trusted to a caveat further up the page, because a caveat
four lines away from a number is the exact separation this file's rule exists to
prevent.

**Reversal trigger, tracked at issue #58:** a reviewer objecting to an encyclopedia
citation for a formal result. That objection is the evidence the primary is
load-bearing after all; absent it we would be paying to verify a citation the paper
has stopped leaning on.

*Sophia and A-MEM were added after a reviewer found them missing, and the reason
they were missing is worth recording, because it was a classification error rather
than an oversight. The sweep that produced this list triaged candidates by whether
they were a person's name, and both are system names — so both were excluded
deliberately. But this bibliography already carries entries for systems (Kumiho,
SCM, GAM): the operative question is whether a citation needs a reference, not
whether it names a person. The sweep was complete over names and the population was
citations.*

*One judgment call, recorded rather than silently made: ACT-R's spreading activation
is cited as a precedent in Ch4 with no source file, and is not covered by the sourced
Anderson & Schooler (1991), which is a different work. It is omitted from the list
above because the text marks it in place as secondary and declines to rest weight on
it. If the final pass decides a flagged-secondary precedent still requires an entry,
this list becomes nineteen.*

## 2026-10-18 — Chapter 5 v2 (stage view): six sources

Sider 1996 and Sider 2000 (author PDFs, tedsider.org), Perry 1972 and Merricks 1994 (author-hosted manuscripts), and the Stanford Encyclopedia entries "Temporal Parts" (Hawley, rev. 2020-05-05) and "Personal Identity" (Olson, rev. 2023-06-30) were found by a source scout on 2026-10-14 and read first-hand by Borges the same day. None of the copies is committed: they are not openly licensed. The manuscripts carry no journal pagination, so the chapter gives no pinpoint pages for them. Lewis 1976 "Survival and Identity" was not found in a legitimate copy and is not cited.
