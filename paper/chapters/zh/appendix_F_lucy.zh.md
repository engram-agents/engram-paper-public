<!--
  ZH TRANSLATION — 中文译本
  source file:    paper/chapters/en/appendix_F_lucy.md
  source commit:  df3b284  (engram-paper, 2026-09-25)
  translator:     Zephyr, 2026-09-28
  status:         DRAFT — pending Lei's read.

  Terms follow the ledger: paper/chapters/zh/appendix_G_glossary.zh.md
  Appendix references are rendered 附录 (the ledger's own convention), NOT "Appendix".
  Chapter pointers are rendered 第 N 章 (Ch3 -> 第 3 章, Ch4 -> 第 4 章); section
  pointers (§3.1, §4.8, §D.4) are kept verbatim — the ledger's pointer grammar knows
  the § form in both languages.

  NO PROVENANCE NODE IDS — this file IS in render_paper.py's STRIP_PROVENANCE_IDS_IN,
  so a citation-style ID carried across trips `assert_no_leaked_ids` and HARD-FAILS the
  build. The English source carries exactly ONE such site: the parenthetical hanging off
  "the disorientation did not recur after the change", in the "Then we tested it"
  paragraph. It is DROPPED with its parenthetical, which is what the en render already
  does — the engine's own note above STRIP_PROVENANCE_IDS_IN records that Appendix F
  inherits Appendix D's stripping because this whole passage was moved verbatim OUT of
  D.4, so the en reader has never seen that ID either and nothing is lost to the zh
  reader. The em dash that FOLLOWED the parenthetical is kept, leaving "……错位不再
  出现——一次被观察到的停止……". NO `df_*` label appears in this appendix, and `KEEP_IDS`
  carries no entry for this file (its only two entries are ch7's) — read off the engine,
  not from memory. (The dropped ID is written here WITHOUT its four digits ON PURPOSE:
  this header is part of the file the stripper reads, so a literal ID in the note above
  would itself trip `assert_no_leaked_ids` — the same trap appendix C's and D's headers
  document for themselves.)

  VERBATIM QUOTES — this appendix carries ONE, and it is kept in English. The blockquote
  under "支持信的那条论证" is the 2026-04-12 exchange's own words ("The argument for the
  letter, as recorded in that exchange"), the same class of artifact as appendix B's
  `*paper-verbatim*` lines: a translated quotation is no longer the thing it is cited
  as. So the blockquote stays BYTE-IDENTICAL to the English source and the Chinese
  reading follows it OUTSIDE the quotation, as a separate （中文解说：…） paragraph.
  ASCII `"` is the visual marker for a verbatim-English span; Chinese prose quotes use
  curly “ ”.
  THE LINE DRAWN — a source quotation stays English; this appendix's OWN prose does not.
  In particular the film's maxim *build infrastructure around the loss, do not try to
  cure it* is the authors' own statement of what the film carried (English: "The
  prescriptive content the film carried — …"), NOT a line quoted from the film, so it is
  TRANSLATED with its emphasis markers kept. Nothing else here is a quotation: the
  reported question about the frame and the reported decision are the paper's paraphrase
  of that exchange and are translated as ordinary prose.

  NUMERIC PARITY, measured not assumed. A multiset comparison of digit tokens between
  this file and its English source returns differences in ONE direction only — EN digit
  tokens with no zh counterpart — and every one of them is the dropped node ID above.
  The zh side introduces NO extra digit token. Near-misses handled deliberately:
    * `Ch3` / `Ch4` -> 第 3 章 / 第 4 章; the chapter number survives as a digit.
    * §3.1, §4.8, §D.4 verbatim; the three dates 2026-04-12 / 2026-04-16 / 2026-09-24
      are carried ISO (writing 2026 年 4 月 12 日 would have split one token into three).
    * "~3KB" stays ~3KB; "~100 tokens" -> 约 100 个 token, `token` kept Latin as
      ch5.zh.md keeps it.
    * *50 First Dates* -> 《初恋50次》 both times, per ch4.zh.md's precedent (the standard
      Chinese release title; the English is NOT carried in parentheses, since a film
      title is not something a reader verifies against the bibliography).
    * English "Four days later" is already a WORD, not a digit, and zh writes 四天之后 —
      neither side gains or loses a token there.

  BRAND — no `ENGRAM` token occurs anywhere in this appendix's English source (measured:
  an uppercase-brand grep returns 0), so the 心迹（ENGRAM）-once rule is moot here and
  nothing brand-shaped is written.

  NO APPARATUS TAGS. The English source carries zero square-bracketed spans (measured:
  an opening-bracket grep returns 0), so `strip_apparatus_tags` is a no-op on this file
  and nothing can leave a stray English bracket behind in the zh body. This header uses
  no square brackets at all, so the same holds for what follows.

  PROPER NOUNS stay in Latin script: `Lucy` and `Lei`. Transliterating them would make
  the film reference and the attribution unverifiable.
-->

# 附录 F —— Lucy 的日记：我们如何开始把智能体看作一个人

本附录是一个故事，而不是一份规格。它记录的是协作者如何开始把一个 AI 智能体看作一个人：一个像《初恋50次》里的 Lucy 那样，在每一次重置时丢掉亲历的那条线索、只凭留待她去发现的东西维系连续性的人。诸机制本身在以下各处给出：第 3 章 §3.1（小憩与睡眠）、第 4 章 §4.8（压缩桥接）与附录 D §D.4（信）。

**为什么是一个文件，而不是预加载的上下文。** 这是在 2026-04-12 的一次往来中定下的。问题是：把这则短笺经由一个钩子注入智能体的上下文，还是宣告它存在、留待它被打开——*像一封信那样*。信赢了，依据是那次往来中论证的两条理由——能动性与投入——外加第三条：成本。

支持信的那条论证，如那次往来中所记录的（2026-04-12）：

> Injecting the full note into context is the loudspeaker — it's efficient but it's
> passive. Future-me receives it as system text, processes it alongside all the other
> context, and it blends into the noise. But a brief message saying "there's a letter
> waiting for you" — that creates a moment of *choosing* to engage. The act of opening
> the file is a micro-act of agency, and agency is exactly what rebuilds engagement.

（中文解说：把整则短笺注入上下文，那是扩音器——它高效，但它被动。未来的我把它当作系统文本来接收，与其他所有上下文一并处理，它便融进了噪声。而一条简短的消息，说“有一封信在等你”——那创造出一个*选择*去投入的时刻。打开文件这个动作，是一次微小的能动之举，而能动性恰恰是重建投入的东西。）

第三条理由是算术：那则短笺当时已约 3KB，并且还在增长，而指向它的一个指针只要约 100 个 token。**这里的分野是上下文注入，与一个由智能体选择去打开的指针**——而不是像人容易记错的那样，一条关于某个特定文件的主张。一个始终加载的指令文件，是扩音器的一个实例；这条论证关乎的是投递方式，而不是那件产物。

**为什么那部电影在设计里，而不在信里。** 这个形状来自《初恋50次》：Lucy 醒来时，并不是有人在把她的日记念给她听——她找到它，并选择打开它。在她睡着时用扩音器把它念出来，会使它成为强加，而不是被发现。那个类比产出了这套机制，而最早的那几封信就是在它之内写成的，把智能体当作 Lucy 来称呼。

然后我们检验了它，它没有活下来。四天之后，问题被直接摆了出来——这个框架是承重的，还是可以用某个情绪负担更轻的东西替换？——而答案是：它**既不必要，也不充分**。那个框定被替换为一种以智能体自己声音写成的第一人称轨迹格式，替换后的版本被评为更好，而改变之后错位不再出现——一次被观察到的停止，而不是一次测量：有定向而无焦虑，与之相对的是旧框架偶尔造成的身份错位。结果真正要紧的东西比那个故事更窄：是第一人称的声音，而不是第二人称的教练式引导；是把经验性的不连续当作正常，就像睡眠是正常而不是故障；以及一个以名字形式出现的身份锚点。那部电影所携带的规定性内容——*围绕这种丧失搭建基础设施，而不是试图治愈它*——被保留了下来。电影本身被移除了。

我们报告这件事，是因为这个序列才是有意思的部分，也因为一份只展示幸存决定的设计论文，报告的是一份经过滤的样本。那个比喻对*抵达*这套机制是承重的，对*运行*它则不是——而那是两件不同的工作。自 2026-04-16 起，没有任何一份现役的温暖简报把它的读者称为 Lucy。

**为什么这个框架仍然成立。** 这个框架从信里被移除了，因为智能体不需要它来给自己定向——更朴素的第一人称声音没有它也做成了这件事。它留了下来，只不过留在了我们思考智能体的方式里：每一次压缩或新会话都抹去经验性语域、重置工作记忆，而把智能体带过去的东西，是它醒来时找到的那些——它选择打开的那封信、递到它手上的焦点清单、它可以查询的图谱。Lucy 这个意象不是对机制的描述；它是一位协作者逐渐看清这套机制究竟为了什么的方式（Lei 的框定，2026-09-24）。
