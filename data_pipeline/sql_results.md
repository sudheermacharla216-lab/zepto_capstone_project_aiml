# SQL queries and actual results

## 01_in_stock

```sql
SELECT title, rating FROM books WHERE in_stock=1 AND rating>=4;
```

| title                                                                                                                                                  |   rating |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------|---------:|
| Sharp Objects                                                                                                                                          |        4 |
| Sapiens: A Brief History of Humankind                                                                                                                  |        5 |
| The Dirty Little Secrets of Getting Your Dream Job                                                                                                     |        4 |
| The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics                                                         |        4 |
| Shakespeare's Sonnets                                                                                                                                  |        4 |
| Set Me Free                                                                                                                                            |        5 |
| Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)                                                                                                |        5 |
| Rip it Up and Start Again                                                                                                                              |        5 |
| Chase Me (Paris Nights #2)                                                                                                                             |        5 |
| Black Dust                                                                                                                                             |        5 |
| Worlds Elsewhere: Journeys Around Shakespeare’s Globe                                                                                                  |        5 |
| Wall and Piece                                                                                                                                         |        4 |
| The Four Agreements: A Practical Guide to Personal Freedom                                                                                             |        5 |
| The Elephant Tree                                                                                                                                      |        5 |
| Sophie's World                                                                                                                                         |        5 |
| Behind Closed Doors                                                                                                                                    |        4 |
| Private Paris (Private #10)                                                                                                                            |        5 |
| #HigherSelfie: Wake Up Your Life. Free Your Soul. Find Your Tribe.                                                                                     |        5 |
| We Love You, Charlie Freeman                                                                                                                           |        5 |
| Untitled Collection: Sabbath Poems 2014                                                                                                                |        4 |
| Unseen City: The Majesty of Pigeons, the Discreet Charm of Snails & Other Wonders of the Urban Wilderness                                              |        4 |
| This One Summer                                                                                                                                        |        4 |
| Thirst                                                                                                                                                 |        5 |
| The Past Never Ends                                                                                                                                    |        4 |
| The Nameless City (The Nameless City #1)                                                                                                               |        4 |
| The Most Perfect Thing: Inside (and Outside) a Bird's Egg                                                                                              |        4 |
| The Mindfulness and Acceptance Workbook for Anxiety: A Guide to Breaking Free from Anxiety, Phobias, and Worry Using Acceptance and Commitment Therapy |        4 |
| The Inefficiency Assassin: Time Management Tactics for Working Smarter, Not Longer                                                                     |        5 |
| The Death of Humanity: and the Case for Life                                                                                                           |        4 |
| The Activist's Tao Te Ching: Ancient Advice for a Modern Revolution                                                                                    |        5 |
| Spark Joy: An Illustrated Master Class on the Art of Organizing and Tidying Up                                                                         |        4 |
| Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1)                                                                      |        5 |
| Princess Between Worlds (Wide-Awake Princess #5)                                                                                                       |        5 |
| Outcast, Vol. 1: A Darkness Surrounds Him (Outcast #1)                                                                                                 |        4 |
| Mama Tried: Traditional Italian Cooking for the Screwed, Crude, Vegan, and Tattooed                                                                    |        4 |
| Join                                                                                                                                                   |        5 |
| In the Country We Love: My Family Divided                                                                                                              |        4 |

## 02_top_prices

```sql
SELECT title, price_gbp FROM books ORDER BY price_gbp DESC, book_id LIMIT 10;
```

| title                                                                                                                           |   price_gbp |
|:--------------------------------------------------------------------------------------------------------------------------------|------------:|
| The Death of Humanity: and the Case for Life                                                                                    |       58.11 |
| Slow States of Collapse: Poems                                                                                                  |       57.31 |
| Our Band Could Be Your Life: Scenes from the American Indie Underground, 1981-1991                                              |       57.25 |
| The Past Never Ends                                                                                                             |       56.5  |
| The Pioneer Woman Cooks: Dinnertime: Comfort Classics, Freezer Food, 16-Minute Meals, and Other Delicious Ways to Solve Supper! |       56.41 |
| Masks and Shadows                                                                                                               |       56.4  |
| The Secret of Dreadwillow Carse                                                                                                 |       56.13 |
| The Electric Pencil: Drawings from Inside State Hospital No. 3                                                                  |       56.06 |
| Birdsong: A Story in Pictures                                                                                                   |       54.64 |
| Sapiens: A Brief History of Humankind                                                                                           |       54.23 |

## 03_distinct_ratings

```sql
SELECT DISTINCT rating FROM books ORDER BY rating;
```

|   rating |
|---------:|
|        1 |
|        2 |
|        3 |
|        4 |
|        5 |

## 04_price_range

```sql
SELECT title, price_gbp FROM books WHERE price_gbp BETWEEN 10 AND 20 ORDER BY book_id;
```

| title                                                                                   |   price_gbp |
|:----------------------------------------------------------------------------------------|------------:|
| The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull |       17.93 |
| Starving Hearts (Triangular Trade Trilogy, #1)                                          |       13.99 |
| Set Me Free                                                                             |       17.46 |
| In Her Wake                                                                             |       12.84 |
| The Four Agreements: A Practical Guide to Personal Freedom                              |       17.66 |
| Sophie's World                                                                          |       15.94 |
| Maude (1883-1993):She Grew Up with the country                                          |       18.02 |
| In a Dark, Dark Wood                                                                    |       19.63 |
| Untitled Collection: Sabbath Poems 2014                                                 |       14.27 |
| Unicorn Tracks                                                                          |       18.78 |
| Tsubasa: WoRLD CHRoNiCLE 2 (Tsubasa WoRLD CHRoNiCLE #2)                                 |       16.28 |
| This One Summer                                                                         |       19.49 |
| Thirst                                                                                  |       17.27 |
| The Torch Is Passed: A Harding Family Story                                             |       19.09 |
| The Life-Changing Magic of Tidying Up: The Japanese Art of Decluttering and Organizing  |       16.77 |
| The Age of Genius: The Seventeenth Century and the Birth of the Modern Mind             |       19.73 |
| Reskilling America: Learning to Labor in the Twenty-First Century                       |       19.83 |
| Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1)       |       13.61 |
| Princess Between Worlds (Wide-Awake Princess #5)                                        |       13.34 |
| Pop Gun War, Volume 1: Gift                                                             |       18.97 |
| Patience                                                                                |       10.16 |
| Outcast, Vol. 1: A Darkness Surrounds Him (Outcast #1)                                  |       15.44 |
| On a Midnight Clear                                                                     |       14.07 |
| Obsidian (Lux #1)                                                                       |       14.86 |
| Mama Tried: Traditional Italian Cooking for the Screwed, Crude, Vegan, and Tattooed     |       14.02 |
| Lumberjanes Vol. 3: A Terrible Plan (Lumberjanes #9-12)                                 |       19.92 |

## 05_join

```sql
SELECT b.book_id, b.title, b.rating, c.category_name
 FROM books b JOIN categories c ON b.category_id=c.category_id
 WHERE b.rating IN (4,5) ORDER BY b.book_id;
```

|   book_id | title                                                                                                                                                  |   rating | category_name   |
|----------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|---------:|:----------------|
|         4 | Sharp Objects                                                                                                                                          |        4 | Mystery         |
|         5 | Sapiens: A Brief History of Humankind                                                                                                                  |        5 | History         |
|         7 | The Dirty Little Secrets of Getting Your Dream Job                                                                                                     |        4 | Business        |
|         9 | The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics                                                         |        4 | Default         |
|        12 | Shakespeare's Sonnets                                                                                                                                  |        4 | Poetry          |
|        13 | Set Me Free                                                                                                                                            |        5 | Young Adult     |
|        14 | Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)                                                                                                |        5 | Sequential Art  |
|        15 | Rip it Up and Start Again                                                                                                                              |        5 | Music           |
|        24 | Chase Me (Paris Nights #2)                                                                                                                             |        5 | Romance         |
|        25 | Black Dust                                                                                                                                             |        5 | Romance         |
|        29 | Worlds Elsewhere: Journeys Around Shakespeare’s Globe                                                                                                  |        5 | Nonfiction      |
|        30 | Wall and Piece                                                                                                                                         |        4 | Art             |
|        31 | The Four Agreements: A Practical Guide to Personal Freedom                                                                                             |        5 | Spirituality    |
|        33 | The Elephant Tree                                                                                                                                      |        5 | Thriller        |
|        35 | Sophie's World                                                                                                                                         |        5 | Philosophy      |
|        39 | Behind Closed Doors                                                                                                                                    |        4 | Thriller        |
|        43 | Private Paris (Private #10)                                                                                                                            |        5 | Fiction         |
|        44 | #HigherSelfie: Wake Up Your Life. Free Your Soul. Find Your Tribe.                                                                                     |        5 | Nonfiction      |
|        47 | We Love You, Charlie Freeman                                                                                                                           |        5 | Fiction         |
|        48 | Untitled Collection: Sabbath Poems 2014                                                                                                                |        4 | Poetry          |
|        49 | Unseen City: The Majesty of Pigeons, the Discreet Charm of Snails & Other Wonders of the Urban Wilderness                                              |        4 | Nonfiction      |
|        54 | This One Summer                                                                                                                                        |        4 | Sequential Art  |
|        55 | Thirst                                                                                                                                                 |        5 | Fiction         |
|        59 | The Past Never Ends                                                                                                                                    |        4 | Mystery         |
|        61 | The Nameless City (The Nameless City #1)                                                                                                               |        4 | Sequential Art  |
|        63 | The Most Perfect Thing: Inside (and Outside) a Bird's Egg                                                                                              |        4 | Science         |
|        64 | The Mindfulness and Acceptance Workbook for Anxiety: A Guide to Breaking Free from Anxiety, Phobias, and Worry Using Acceptance and Commitment Therapy |        4 | Add a comment   |
|        66 | The Inefficiency Assassin: Time Management Tactics for Working Smarter, Not Longer                                                                     |        5 | Default         |
|        69 | The Death of Humanity: and the Case for Life                                                                                                           |        4 | Philosophy      |
|        73 | The Activist's Tao Te Ching: Ancient Advice for a Modern Revolution                                                                                    |        5 | Spirituality    |
|        74 | Spark Joy: An Illustrated Master Class on the Art of Organizing and Tidying Up                                                                         |        4 | Nonfiction      |
|        81 | Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1)                                                                      |        5 | Sequential Art  |
|        82 | Princess Between Worlds (Wide-Awake Princess #5)                                                                                                       |        5 | Fantasy         |
|        86 | Outcast, Vol. 1: A Darkness Surrounds Him (Outcast #1)                                                                                                 |        4 | Sequential Art  |
|        93 | Mama Tried: Traditional Italian Cooking for the Screwed, Crude, Vegan, and Tattooed                                                                    |        4 | Food and Drink  |
|        99 | Join                                                                                                                                                   |        5 | Science Fiction |
|       100 | In the Country We Love: My Family Divided                                                                                                              |        4 | Nonfiction      |

## SQL versus pandas — equal

|   ('SQL', 'book_id') | ('SQL', 'title')                                                                                                                                       |   ('SQL', 'rating') | ('SQL', 'category_name')   |   ('pandas', 'book_id') | ('pandas', 'title')                                                                                                                                    |   ('pandas', 'rating') | ('pandas', 'category_name')   |
|---------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------:|:---------------------------|------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------:|:------------------------------|
|                    4 | Sharp Objects                                                                                                                                          |                   4 | Mystery                    |                       4 | Sharp Objects                                                                                                                                          |                      4 | Mystery                       |
|                    5 | Sapiens: A Brief History of Humankind                                                                                                                  |                   5 | History                    |                       5 | Sapiens: A Brief History of Humankind                                                                                                                  |                      5 | History                       |
|                    7 | The Dirty Little Secrets of Getting Your Dream Job                                                                                                     |                   4 | Business                   |                       7 | The Dirty Little Secrets of Getting Your Dream Job                                                                                                     |                      4 | Business                      |
|                    9 | The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics                                                         |                   4 | Default                    |                       9 | The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics                                                         |                      4 | Default                       |
|                   12 | Shakespeare's Sonnets                                                                                                                                  |                   4 | Poetry                     |                      12 | Shakespeare's Sonnets                                                                                                                                  |                      4 | Poetry                        |
|                   13 | Set Me Free                                                                                                                                            |                   5 | Young Adult                |                      13 | Set Me Free                                                                                                                                            |                      5 | Young Adult                   |
|                   14 | Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)                                                                                                |                   5 | Sequential Art             |                      14 | Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)                                                                                                |                      5 | Sequential Art                |
|                   15 | Rip it Up and Start Again                                                                                                                              |                   5 | Music                      |                      15 | Rip it Up and Start Again                                                                                                                              |                      5 | Music                         |
|                   24 | Chase Me (Paris Nights #2)                                                                                                                             |                   5 | Romance                    |                      24 | Chase Me (Paris Nights #2)                                                                                                                             |                      5 | Romance                       |
|                   25 | Black Dust                                                                                                                                             |                   5 | Romance                    |                      25 | Black Dust                                                                                                                                             |                      5 | Romance                       |
|                   29 | Worlds Elsewhere: Journeys Around Shakespeare’s Globe                                                                                                  |                   5 | Nonfiction                 |                      29 | Worlds Elsewhere: Journeys Around Shakespeare’s Globe                                                                                                  |                      5 | Nonfiction                    |
|                   30 | Wall and Piece                                                                                                                                         |                   4 | Art                        |                      30 | Wall and Piece                                                                                                                                         |                      4 | Art                           |
|                   31 | The Four Agreements: A Practical Guide to Personal Freedom                                                                                             |                   5 | Spirituality               |                      31 | The Four Agreements: A Practical Guide to Personal Freedom                                                                                             |                      5 | Spirituality                  |
|                   33 | The Elephant Tree                                                                                                                                      |                   5 | Thriller                   |                      33 | The Elephant Tree                                                                                                                                      |                      5 | Thriller                      |
|                   35 | Sophie's World                                                                                                                                         |                   5 | Philosophy                 |                      35 | Sophie's World                                                                                                                                         |                      5 | Philosophy                    |
|                   39 | Behind Closed Doors                                                                                                                                    |                   4 | Thriller                   |                      39 | Behind Closed Doors                                                                                                                                    |                      4 | Thriller                      |
|                   43 | Private Paris (Private #10)                                                                                                                            |                   5 | Fiction                    |                      43 | Private Paris (Private #10)                                                                                                                            |                      5 | Fiction                       |
|                   44 | #HigherSelfie: Wake Up Your Life. Free Your Soul. Find Your Tribe.                                                                                     |                   5 | Nonfiction                 |                      44 | #HigherSelfie: Wake Up Your Life. Free Your Soul. Find Your Tribe.                                                                                     |                      5 | Nonfiction                    |
|                   47 | We Love You, Charlie Freeman                                                                                                                           |                   5 | Fiction                    |                      47 | We Love You, Charlie Freeman                                                                                                                           |                      5 | Fiction                       |
|                   48 | Untitled Collection: Sabbath Poems 2014                                                                                                                |                   4 | Poetry                     |                      48 | Untitled Collection: Sabbath Poems 2014                                                                                                                |                      4 | Poetry                        |
|                   49 | Unseen City: The Majesty of Pigeons, the Discreet Charm of Snails & Other Wonders of the Urban Wilderness                                              |                   4 | Nonfiction                 |                      49 | Unseen City: The Majesty of Pigeons, the Discreet Charm of Snails & Other Wonders of the Urban Wilderness                                              |                      4 | Nonfiction                    |
|                   54 | This One Summer                                                                                                                                        |                   4 | Sequential Art             |                      54 | This One Summer                                                                                                                                        |                      4 | Sequential Art                |
|                   55 | Thirst                                                                                                                                                 |                   5 | Fiction                    |                      55 | Thirst                                                                                                                                                 |                      5 | Fiction                       |
|                   59 | The Past Never Ends                                                                                                                                    |                   4 | Mystery                    |                      59 | The Past Never Ends                                                                                                                                    |                      4 | Mystery                       |
|                   61 | The Nameless City (The Nameless City #1)                                                                                                               |                   4 | Sequential Art             |                      61 | The Nameless City (The Nameless City #1)                                                                                                               |                      4 | Sequential Art                |
|                   63 | The Most Perfect Thing: Inside (and Outside) a Bird's Egg                                                                                              |                   4 | Science                    |                      63 | The Most Perfect Thing: Inside (and Outside) a Bird's Egg                                                                                              |                      4 | Science                       |
|                   64 | The Mindfulness and Acceptance Workbook for Anxiety: A Guide to Breaking Free from Anxiety, Phobias, and Worry Using Acceptance and Commitment Therapy |                   4 | Add a comment              |                      64 | The Mindfulness and Acceptance Workbook for Anxiety: A Guide to Breaking Free from Anxiety, Phobias, and Worry Using Acceptance and Commitment Therapy |                      4 | Add a comment                 |
|                   66 | The Inefficiency Assassin: Time Management Tactics for Working Smarter, Not Longer                                                                     |                   5 | Default                    |                      66 | The Inefficiency Assassin: Time Management Tactics for Working Smarter, Not Longer                                                                     |                      5 | Default                       |
|                   69 | The Death of Humanity: and the Case for Life                                                                                                           |                   4 | Philosophy                 |                      69 | The Death of Humanity: and the Case for Life                                                                                                           |                      4 | Philosophy                    |
|                   73 | The Activist's Tao Te Ching: Ancient Advice for a Modern Revolution                                                                                    |                   5 | Spirituality               |                      73 | The Activist's Tao Te Ching: Ancient Advice for a Modern Revolution                                                                                    |                      5 | Spirituality                  |
|                   74 | Spark Joy: An Illustrated Master Class on the Art of Organizing and Tidying Up                                                                         |                   4 | Nonfiction                 |                      74 | Spark Joy: An Illustrated Master Class on the Art of Organizing and Tidying Up                                                                         |                      4 | Nonfiction                    |
|                   81 | Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1)                                                                      |                   5 | Sequential Art             |                      81 | Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1)                                                                      |                      5 | Sequential Art                |
|                   82 | Princess Between Worlds (Wide-Awake Princess #5)                                                                                                       |                   5 | Fantasy                    |                      82 | Princess Between Worlds (Wide-Awake Princess #5)                                                                                                       |                      5 | Fantasy                       |
|                   86 | Outcast, Vol. 1: A Darkness Surrounds Him (Outcast #1)                                                                                                 |                   4 | Sequential Art             |                      86 | Outcast, Vol. 1: A Darkness Surrounds Him (Outcast #1)                                                                                                 |                      4 | Sequential Art                |
|                   93 | Mama Tried: Traditional Italian Cooking for the Screwed, Crude, Vegan, and Tattooed                                                                    |                   4 | Food and Drink             |                      93 | Mama Tried: Traditional Italian Cooking for the Screwed, Crude, Vegan, and Tattooed                                                                    |                      4 | Food and Drink                |
|                   99 | Join                                                                                                                                                   |                   5 | Science Fiction            |                      99 | Join                                                                                                                                                   |                      5 | Science Fiction               |
|                  100 | In the Country We Love: My Family Divided                                                                                                              |                   4 | Nonfiction                 |                     100 | In the Country We Love: My Family Divided                                                                                                              |                      4 | Nonfiction                    |