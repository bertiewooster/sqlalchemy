from curses import echo

from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

# Trivial connection
# with engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all())

# Create table
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))

# Insert data and then commit changes
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()

# "Begin once": Declare to be a transaction block
#   to automatically COMMIT if successful, or ROLLBACK if exception raised
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )

# Read and print data from rows
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    # for row in result:
    #     print(f"x: {row.x} y: {row.y}")

    # Access data in Pythonic style: as tuples
    # print("x", "y")
    # for x, y in result:
    #     print(x, y)

    # Access data by attribute name
    # for row in result:
    #     y = row.y
    #     print(f"Row: {row.x} {y}")

    # Put data into dictionary aka mapping access
    for dict_row in result.mappings():
        x = dict_row["x"]
        y = dict_row["y"]
        print(x, y)

# Sending Parameters
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x} y: {row.y}")

