# planning.md

## Project Title

WallStreetBets Reddit Post Discourse Classification

## 1. Community

The community chosen for this project is r/wallstreetbets, a Reddit community where users discuss stock trading, options trading, market news, gains, losses, memes, and speculative investment ideas. This community is a strong fit for a classification task because the discourse is active, text-heavy, and varies sharply in quality: some posts contain detailed trading analysis, some are emotional reactions to market movement, some are memes or hype posts, and some are about subreddit/community events or moderation.

These distinctions matter because WallStreetBets users treat different kinds of posts very differently. A due-diligence style post is expected to contain reasoning, evidence, ticker analysis, risk discussion, or a trade thesis, while a hype post or meme post is judged more by entertainment value and community tone. A useful classifier should separate posts that are trying to inform trading decisions from posts that are mainly reacting, joking, or discussing the subreddit itself.

## 2. Dataset Columns and How I Will Use Them

The original dataset contains these columns:

| Column      | Meaning                              | Use in this project                                          |
| ----------- | ------------------------------------ | ------------------------------------------------------------ |
| `id`        | Reddit post ID                       | Keep as a unique identifier. Do not use as a model feature.  |
| `title`     | Title of the Reddit post             | Main text input for classification.                          |
| `body`      | Body/self-text of the post           | Secondary text input. Missing values will be replaced with an empty string. |
| `score`     | Reddit score/upvotes minus downvotes | Metadata only. It can be used for analysis, but not as a main text feature because it may leak popularity instead of discourse type. |
| `url`       | URL attached to the post             | Keep for traceability. Do not use directly as a model feature. |
| `comms_num` | Number of comments                   | Metadata only. It can show engagement, but it should not decide the discourse label. |
| `created`   | Unix timestamp                       | Metadata only. Useful for sorting or trend analysis.         |
| `timestamp` | Human-readable date/time             | Metadata only. Useful for trend analysis and train/test splitting by time. |

I will create two new columns:

| New column | Meaning                                                      |
| ---------- | ------------------------------------------------------------ |
| `text`     | Combined text field created as `title + " " + body`.         |
| `label`    | Human-assigned discourse label. This is the target variable for the classifier. |

The classifier should mainly use `text` as the input. The `label` column will contain exactly one of the four label strings defined below.

## 3. Labels

I will use four mutually exclusive labels. Each post should receive exactly one label based on the author's primary purpose.

### Label 1: `trade_analysis`

Definition: A post belongs to `trade_analysis` when its main purpose is to explain, justify, or evaluate a stock, option, market move, or trading strategy using reasoning, evidence, numbers, screenshots, ticker discussion, or a clear thesis.

Clear example A: A user writes a long post explaining why they believe GME is undervalued, discusses short interest, price action, catalysts, and says what position they are taking.

Clear example B: A user analyzes AMC call options, explains their expiration date, strike price, risk, and why they think the trade could work.

Uncertain case: A post says “NOK will moon next week because volume is increasing” with one chart and very little explanation. I would label it `trade_analysis` only if the post gives a real reason or evidence; otherwise, it belongs in `market_reaction_or_hype`.

### Label 2: `market_reaction_or_hype`

Definition: A post belongs to `market_reaction_or_hype` when its main purpose is to react emotionally to market movement, hype a ticker, celebrate gains, panic about losses, or encourage buying/selling without substantial analysis.

Clear example A: A user posts “GME TO THE MOON, HOLD THE LINE” with no real explanation beyond excitement.

Clear example B: A user reacts to AMC dropping sharply and writes that everyone is doomed or that they are still holding no matter what.

Uncertain case: A post celebrates a large gain and briefly mentions the trade that caused it. I would label it `market_reaction_or_hype` if the focus is the emotional reaction or celebration, not a reasoned explanation of the trade.

### Label 3: `meme_or_shitpost`

Definition: A post belongs to `meme_or_shitpost` when its main purpose is humor, sarcasm, community slang, absurdity, or entertainment rather than serious trading discussion.

Clear example A: A user posts a joke title comparing their portfolio to a burning dumpster with no meaningful trading claim.

Clear example B: A user writes a fake motivational speech about losing money on options for comedic effect.

Uncertain case: A meme uses a real ticker like GME or AMC and also contains a bullish claim. I would label it `meme_or_shitpost` if the main purpose is clearly the joke or meme format, not the trading claim.

### Label 4: `community_meta_or_news`

Definition: A post belongs to `community_meta_or_news` when its main purpose is to discuss the subreddit, moderation, daily discussion threads, media attention, platform issues, rules, or external news about WallStreetBets rather than a specific personal trade or thesis.

Clear example A: A daily trading discussion thread tells users to keep general market discussion in one place and links to subreddit resources.

Clear example B: A post discusses news coverage of WallStreetBets after the GameStop event and asks how the subreddit has changed.

Uncertain case: A post shares news about a company and users discuss whether to buy the stock. I would label it `community_meta_or_news` only if the focus is the news item or community response; if the author uses the news to argue for a trade, I would label it `trade_analysis`.

## 4. Mutual Exclusivity Rule

Each post will be labeled by its primary purpose, not by every topic it mentions. If a post includes multiple elements, I will ask what the author mainly wants the community to do:

- If the author wants readers to understand or evaluate a trade idea, label it `trade_analysis`.
- If the author wants readers to react emotionally, hold, buy, panic, celebrate, or hype, label it `market_reaction_or_hype`.
- If the author mainly wants to entertain or joke, label it `meme_or_shitpost`.
- If the author mainly wants to discuss the subreddit, rules, daily threads, media coverage, or general community context, label it `community_meta_or_news`.

## 5. Hard Edge Cases

The hardest edge case is a post that uses meme language while also making a real trading claim about a stock such as GME, AMC, NOK, or BB.

This type of post could belong to either `meme_or_shitpost` or `market_reaction_or_hype`. It may also sometimes look like `trade_analysis` if it mentions a ticker, price target, or position.

Decision rule: If the post contains a clear trade thesis with reasoning or evidence, label it `trade_analysis`; if it mainly pushes emotion or group action with little reasoning, label it `market_reaction_or_hype`; if the joke format is the main point, label it `meme_or_shitpost`.

Example: A post titled “GME rocket fuel loaded, apes never sell” with no body text would be labeled `market_reaction_or_hype` because it is mainly a hype/holding message, not analysis. A post with the same title but a long body explaining short interest, catalysts, risk, and position sizing would be labeled `trade_analysis`.

### Difficult examples encountered during annotation

These are real cases from annotation that gave me genuine pause (Milestone 3).

**Difficult example 1: Fake/ironic DD vs. genuine trade analysis**
- **Row / ID:** candidates_trade_analysis row 11, `o64enf`
- **Post type:** A “Marble ETF” post describes picking stocks using marbles and a gravity-style game.
- **Possible labels:** `trade_analysis` vs. `meme_or_shitpost`
- **Why it is difficult:** It uses DD language and claims to select stocks, but the method is intentionally absurd and entertainment-driven rather than a serious trading thesis.
- **Final label:** `meme_or_shitpost`
- **Decision rule used:** If a post uses DD structure but the actual reasoning is intentionally absurd, parody-like, or mainly for entertainment, label it `meme_or_shitpost` instead of `trade_analysis`.

**Difficult example 2: Simple squeeze math vs. hype**
- **Row / ID:** candidates_trade_analysis row 14, `mcf7u1`
- **Post type:** The post estimates how many GME/AMC shares WSB users might collectively hold and argues that if people keep holding, sellers will have to pay extreme prices.
- **Possible labels:** `trade_analysis` vs. `market_reaction_or_hype`
- **Why it is difficult:** The post uses rough numbers and a float-ownership argument, but the tone and purpose are also strongly “hold forever” hype.
- **Final label:** `trade_analysis`
- **Decision rule used:** If the post gives a concrete market mechanism, even with rough math, label it `trade_analysis`; if it only says to hold or go to the moon without reasoning, label it `market_reaction_or_hype`.

**Difficult example 3: YOLO update vs. meme/shitpost**
- **Row / ID:** candidates_trade_analysis row 58, `lgx0fn`
- **Post type:** An AMD YOLO update presents positions and calls itself DD, but the body relies heavily on joking language about tendy gods, Valhalla, and hype rather than actual analysis.
- **Possible labels:** `trade_analysis` vs. `meme_or_shitpost` vs. `market_reaction_or_hype`
- **Why it is difficult:** It includes real positions and a ticker, but the main function is comedic performance and YOLO entertainment, not a reasoned stock argument.
- **Final label:** `meme_or_shitpost`
- **Decision rule used:** A real ticker or position does not make a post `trade_analysis`; if the main value of the post is absurdity, parody, or comic community performance, label it `meme_or_shitpost`.

## 6. Data Collection and Annotation Plan

The dataset already contains about 53,200 Reddit posts from r/wallstreetbets. For this project, I will annotate a smaller balanced sample instead of using all rows immediately.

I will begin by reading 30–40 random posts from the dataset before finalizing the labels. After that, I will manually annotate at least 200 examples. I will aim for a balanced dataset with about 50 posts per label:

| Label                     | Target count |
| ------------------------- | -----------: |
| `trade_analysis`          |           50 |
| `market_reaction_or_hype` |           50 |
| `meme_or_shitpost`        |           50 |
| `community_meta_or_news`  |           50 |

If one label is underrepresented after the first 200 examples, I will oversample likely candidates using keywords and patterns. For example, posts containing “DD,” “calls,” “puts,” “position,” or ticker symbols may help find `trade_analysis`; posts containing “moon,” “hold,” “diamond hands,” or “tendies” may help find `market_reaction_or_hype`; posts with very short joke-like titles may help find `meme_or_shitpost`; and daily discussion or moderator-style posts may help find `community_meta_or_news`.

I will still manually verify every label. Keyword search will only help find candidates; it will not automatically assign the final label.

## 7. Evaluation Metrics

Accuracy alone is not enough because the labels may be imbalanced and some mistakes are more important than others. I will use these metrics:

| Metric              | Why it matters                                               |
| ------------------- | ------------------------------------------------------------ |
| Accuracy            | Gives the overall percentage of correct predictions.         |
| Macro F1-score      | Treats all labels equally, which matters if some labels are less common. |
| Per-label precision | Shows whether the model is over-predicting a label.          |
| Per-label recall    | Shows whether the model is missing a label.                  |
| Confusion matrix    | Shows which labels are being confused, especially `meme_or_shitpost` vs. `market_reaction_or_hype` and `trade_analysis` vs. `market_reaction_or_hype`. |

Macro F1-score is especially important because I want the classifier to work across all discourse types, not only the most common one.

## 8. Definition of Success

A useful classifier should reach at least 75% accuracy and at least 0.70 macro F1-score on a held-out test set. It should also achieve at least 0.65 F1-score on every individual label so that it is not ignoring smaller or harder categories.

For a real community tool, I would consider the model good enough if it can reliably separate serious trading analysis from hype, memes, and community-meta posts. The most important practical success condition is that `trade_analysis` should have high precision, ideally 0.75 or higher, because users looking for serious discussion should not be shown mostly memes or hype posts.

## 9. AI Tool Plan

### Label stress-testing

Before annotating all 200 examples, I will give an AI tool my four label definitions and ask it to generate 5–10 borderline WallStreetBets-style posts. I will specifically ask for examples that sit between:

- `trade_analysis` and `market_reaction_or_hype`
- `market_reaction_or_hype` and `meme_or_shitpost`
- `community_meta_or_news` and `trade_analysis`

If I cannot classify those generated examples consistently, I will tighten the definitions and decision rules before continuing annotation.

### Annotation assistance

I may use an LLM to pre-label a batch of examples, but I will treat those labels only as suggestions. Every pre-labeled example will still be reviewed manually before it enters the final training dataset.

If I use AI pre-labeling, I will add another column called `ai_prelabeled` with values `yes` or `no`, and possibly another column called `ai_suggested_label`. The final human-reviewed label will remain in the `label` column.

### Failure analysis

After training the model, I will collect the incorrect predictions from the validation or test set and give them to an AI tool to identify common failure patterns. I will look for repeated issues such as:

- Meme posts being mistaken for hype posts.
- Hype posts being mistaken for trade analysis because they mention ticker symbols.
- News posts being mistaken for trade analysis because they discuss a company.
- Very short titles being hard to classify without body text.

I will verify these patterns myself by reading the misclassified examples directly before including them in the final project write-up.

## 10. Final Label Map

The final label map for the project is:

```python
LABEL_MAP = {
    "trade_analysis": 0,
    "market_reaction_or_hype": 1,
    "meme_or_shitpost": 2,
    "community_meta_or_news": 3,
}
```

The final dataset should contain at least these columns:

| Column      | Required? | Description                                                  |
| ----------- | --------- | ------------------------------------------------------------ |
| `id`        | Yes       | Original Reddit post ID.                                     |
| `title`     | Yes       | Original post title.                                         |
| `body`      | Yes       | Original post body, with missing values replaced by empty strings. |
| `text`      | Yes       | Combined title and body text used as model input.            |
| `label`     | Yes       | One of the four final labels.                                |
| `score`     | Optional  | Metadata for analysis.                                       |
| `comms_num` | Optional  | Metadata for analysis.                                       |
| `timestamp` | Optional  | Metadata for trend/time analysis.                            |
| `url`       | Optional  | Link for traceability.                                       |
