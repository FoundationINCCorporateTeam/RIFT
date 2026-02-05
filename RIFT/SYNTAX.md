# RIFT Language Syntax Definition

**Version:** 2.0  
**Last Updated:** 2026-02-05

## Table of Contents

1. [Introduction](#introduction)
2. [Lexical Structure](#lexical-structure)
3. [Grammar Specification](#grammar-specification)
4. [Type System](#type-system)
5. [Operators](#operators)
6. [Control Flow](#control-flow)
7. [Functions](#functions)
8. [Classes and Objects](#classes-and-objects)
9. [Pattern Matching](#pattern-matching)
10. [Module System](#module-system)
11. [Error Handling](#error-handling)
12. [Asynchronous Programming](#asynchronous-programming)
13. [Standard Library](#standard-library)
14. [Complete Examples](#complete-examples)

---

## Introduction

RIFT (Rapid Integrated Framework Technology) is a modern, dynamically-typed programming language that combines the best features of PHP, JavaScript, and Python with enterprise-grade built-in capabilities. RIFT uses unique character delimiters to create a distinctive visual syntax:

- **Blocks:** `@` (open) and `#` (close) instead of `{` and `}`
- **Arrays/Lists:** `~` (open) and `!` (close) instead of `[` and `]`
- **Parentheses:** `(` and `)` remain unchanged

---

## Lexical Structure

### 2.1 Character Set

RIFT source files are encoded in UTF-8. The language uses ASCII characters with special delimiters:

- **Block delimiters:** `@` `#`
- **Array delimiters:** `~` `!`
- **Grouping delimiters:** `(` `)`

### 2.2 Comments

```rift
# Single-line comment

/* Multi-line
   comment */
```

### 2.3 Identifiers

**Syntax:**
```
identifier ::= (letter | '_') (letter | digit | '_')*
letter     ::= 'a'..'z' | 'A'..'Z'
digit      ::= '0'..'9'
```

**Examples:**
```rift
myVariable
_privateVar
userName123
```

**Rules:**
- Must start with a letter or underscore
- Can contain letters, digits, and underscores
- Case-sensitive
- Cannot be a reserved keyword

### 2.4 Keywords

RIFT reserves the following keywords:

| Category | Keywords |
|----------|----------|
| **Declarations** | `let`, `mut`, `const`, `conduit`, `make` |
| **Control Flow** | `if`, `else`, `while`, `repeat`, `check`, `when` |
| **Loop Control** | `stop`, `next` |
| **Functions** | `give`, `yield` |
| **Classes** | `build`, `extend`, `me`, `parent`, `static`, `get`, `set` |
| **Modules** | `grab`, `share`, `as` |
| **Error Handling** | `try`, `catch`, `finally`, `fail` |
| **Async** | `async`, `wait` |
| **Operators** | `and`, `or`, `not`, `in` |
| **Literals** | `yes`, `no`, `none` |

### 2.5 Literals

#### 2.5.1 Boolean Literals

```rift
yes    # true
no     # false
```

#### 2.5.2 Null Literal

```rift
none   # null/nil/undefined
```

#### 2.5.3 Numeric Literals

```rift
# Decimal integers
42
1_000_000

# Decimal floating-point
3.14159
2.5e10
1.5e-5

# Hexadecimal
0xFF
0x1A2B

# Binary
0b1010
0b1111_0000
```

#### 2.5.4 String Literals

```rift
# Single-quoted strings
'Hello, World!'
'Line 1\nLine 2'

# Double-quoted strings
"Hello, World!"
"Tab\tSeparated"

# Template strings (with interpolation)
`Hello, $@name#!`
`Result: $@x + y#`
`Nested: $@user.name.toUpper()#`
```

**Escape sequences:**
- `\n` - newline
- `\t` - tab
- `\r` - carriage return
- `\\` - backslash
- `\'` - single quote
- `\"` - double quote
- `\0` - null character

#### 2.5.5 Array Literals

```rift
~!                    # Empty array
~1, 2, 3!            # Numeric array
~"a", "b", "c"!      # String array
~1, "two", yes!      # Mixed types
~1, 2, ...rest!      # Spread operator
```

#### 2.5.6 Map Literals (Objects/Dictionaries)

```rift
@#                           # Empty map
@name: "Alice", age: 30#     # Simple map
@
    firstName: "Alice",
    lastName: "Smith",
    age: 30,
    active: yes
#

# Computed property names
@~key!: value#

# Shorthand property
let name = "Alice"
@name#  # Equivalent to @name: name#
```

### 2.6 Operators and Punctuation

**Arithmetic:** `+`, `-`, `*`, `/`, `%`, `**`  
**Comparison:** `==`, `!=`, `~`, `!`, `~=`, `!=`  
**Logical:** `and`, `or`, `not`  
**Assignment:** `=`, `+=`, `-=`, `*=`, `/=`  
**Special:** `??`, `?.`, `?~`, `-!`, `~-`, `~!`, `=!`, `::`, `..`, `...`  
**Delimiters:** `@`, `#`, `~`, `!`, `(`, `)`, `,`, `.`, `:`, `;`, `?`, `@`

---

## Grammar Specification

### 3.1 Program Structure

```bnf
program        ::= statement*

statement      ::= declaration
                 | expression_stmt
                 | control_flow
                 | block
                 | import_stmt
                 | export_stmt

block          ::= '@' statement* '#'
```

### 3.2 Declarations

```bnf
declaration    ::= var_decl
                 | const_decl
                 | function_decl
                 | class_decl

var_decl       ::= ('let' | 'mut') IDENTIFIER (':' type)? ('=' expression)? ';'?
const_decl     ::= 'const' IDENTIFIER (':' type)? '=' expression ';'?
function_decl  ::= 'conduit' IDENTIFIER '(' parameters? ')' (':' type)? block
class_decl     ::= 'make' IDENTIFIER ('extend' IDENTIFIER)? '@' class_body '#'

parameters     ::= parameter (',' parameter)*
parameter      ::= IDENTIFIER (':' type)? ('=' expression)?
```

### 3.3 Expressions

```bnf
expression     ::= assignment
assignment     ::= IDENTIFIER '=' expression
                 | pipeline
pipeline       ::= null_coalesce ('-!' null_coalesce)*
null_coalesce  ::= logical_or ('??' logical_or)*
logical_or     ::= logical_and ('or' logical_and)*
logical_and    ::= equality ('and' equality)*
equality       ::= comparison (('==' | '!=') comparison)*
comparison     ::= range (('~' | '!' | '~=' | '!=') range)*
range          ::= additive ('..' additive)?
additive       ::= multiplicative (('+' | '-') multiplicative)*
multiplicative ::= power (('*' | '/' | '%') power)*
power          ::= unary ('**' unary)*
unary          ::= ('not' | '-' | '+') unary
                 | postfix
postfix        ::= primary (call | member | index)*
call           ::= '(' arguments? ')'
member         ::= '.' IDENTIFIER
                 | '?.' IDENTIFIER
index          ::= '~' expression '!'
                 | '?~' expression '!'
primary        ::= literal
                 | IDENTIFIER
                 | '(' expression ')'
                 | lambda
                 | array_literal
                 | map_literal
```

### 3.4 Control Flow

```bnf
if_stmt        ::= 'if' expression block ('else' (if_stmt | block))?
while_stmt     ::= 'while' expression block
repeat_stmt    ::= 'repeat' pattern 'in' expression block
check_stmt     ::= 'check' expression '@' case_clause* '#'
case_clause    ::= pattern ('when' expression)? '=!' (expression | block)
```

---

## Type System

### 4.1 Built-in Types

| Type | Description | Example |
|------|-------------|---------|
| `num` | Numbers (int/float) | `42`, `3.14` |
| `text` | Strings | `"hello"` |
| `bool` | Booleans | `yes`, `no` |
| `list` | Arrays | `~1, 2, 3!` |
| `map` | Objects/Dictionaries | `@key: "value"#` |
| `none` | Null/undefined | `none` |
| `conduit` | Functions | `(x) =! x * 2` |

### 4.2 Type Annotations

Type annotations are optional and provide runtime type checking:

```rift
let name: text = "Alice"
let age: num = 30
let active: bool = yes
let items: list = ~1, 2, 3!
let user: map = @name: "Alice"#

conduit add(a: num, b: num): num @
    give a + b
#
```

### 4.3 Type Checking

RIFT performs runtime type checking when type annotations are present:

```rift
let x: num = "hello"  # Runtime error: Type mismatch
```

---

## Operators

### 5.1 Operator Precedence

From highest to lowest precedence:

| Level | Operators | Description | Associativity |
|-------|-----------|-------------|---------------|
| 1 | `()`, `~!`, `.`, `?.` | Grouping, indexing, member access | Left |
| 2 | `**` | Exponentiation | Right |
| 3 | `not`, `-`, `+` | Unary operators | Right |
| 4 | `*`, `/`, `%` | Multiplicative | Left |
| 5 | `+`, `-` | Additive | Left |
| 6 | `..` | Range | Left |
| 7 | `~`, `!`, `~=`, `!=` | Comparison | Left |
| 8 | `==`, `!=` | Equality | Left |
| 9 | `and` | Logical AND | Left |
| 10 | `or` | Logical OR | Left |
| 11 | `??` | Null coalescing | Left |
| 12 | `-!`, `~!` | Pipeline | Left |
| 13 | `=!` | Lambda arrow | Right |
| 14 | `=`, `+=`, `-=`, `*=`, `/=` | Assignment | Right |

### 5.2 Arithmetic Operators

```rift
let a = 10 + 5      # Addition: 15
let b = 10 - 5      # Subtraction: 5
let c = 10 * 5      # Multiplication: 50
let d = 10 / 5      # Division: 2
let e = 10 % 3      # Modulo: 1
let f = 2 ** 8      # Exponentiation: 256
```

### 5.3 Comparison Operators

```rift
10 == 10    # Equal: yes
10 != 5     # Not equal: yes
10 ~ 20     # Less than: yes
10 ! 5      # Greater than: yes
10 ~= 10    # Less or equal: yes
10 != 5     # Greater or equal: yes
```

### 5.4 Logical Operators

```rift
yes and no      # Logical AND: no
yes or no       # Logical OR: yes
not yes         # Logical NOT: no
```

### 5.5 Special Operators

#### Null Coalescing (`??`)

```rift
let value = maybeNull ?? "default"
```

#### Safe Navigation (`?.`)

```rift
let name = user?.profile?.name
```

#### Safe Indexing (`?~`)

```rift
let item = array?~0!
```

#### Pipeline (`-!`)

```rift
let result = data
    -! filter((x) =! x ! 10)
    -! map((x) =! x * 2)
    -! sum()
```

#### Async Pipeline (`~!`)

```rift
let result = wait fetchData()
    ~! processData
    ~! saveData
```

#### Lambda Arrow (`=!`)

```rift
let double = (x) =! x * 2
let add = (a, b) =! a + b
```

#### Static Access (`::`)

```rift
Math::PI
String::fromCharCode(65)
```

#### Range (`..`)

```rift
repeat i in 1..10 @
    print(i)
#
```

#### Spread (`...`)

```rift
let arr1 = ~1, 2, 3!
let arr2 = ~...arr1, 4, 5!  # ~1, 2, 3, 4, 5!

conduit sum(...numbers) @
    give numbers -! reduce((a, b) =! a + b, 0)
#
```

---

## Control Flow

### 6.1 If-Else Statements

```rift
if score != 90 @
    print("A")
# else if score != 80 @
    print("B")
# else if score != 70 @
    print("C")
# else @
    print("F")
#
```

### 6.2 While Loops

```rift
mut count = 0
while count ~ 10 @
    print(count)
    count = count + 1
#
```

### 6.3 Repeat Loops (For Loops)

#### Iterate over array

```rift
let items = ~"apple", "banana", "cherry"!
repeat item in items @
    print(item)
#
```

#### Iterate with index

```rift
repeat (index, item) in items @
    print(`$@index#: $@item#`)
#
```

#### Range iteration

```rift
repeat i in 1..10 @
    print(i)
#

repeat i in 0..100 @
    if i % 2 == 0 @
        print(i)
    #
#
```

### 6.4 Loop Control

```rift
repeat i in 1..100 @
    if i % 7 == 0 @
        stop  # Break out of loop
    #
    
    if i % 2 == 0 @
        next  # Continue to next iteration
    #
    
    print(i)
#
```

---

## Functions

### 7.1 Function Declaration

```rift
conduit greet(name) @
    give `Hello, $@name#!`
#

conduit add(a, b) @
    give a + b
#
```

### 7.2 Type Annotations

```rift
conduit multiply(a: num, b: num): num @
    give a * b
#
```

### 7.3 Default Parameters

```rift
conduit greet(name = "World") @
    give `Hello, $@name#!`
#

print(greet())          # "Hello, World!"
print(greet("Alice"))   # "Hello, Alice!"
```

### 7.4 Rest Parameters

```rift
conduit sum(...numbers) @
    mut total = 0
    repeat n in numbers @
        total = total + n
    #
    give total
#

print(sum(1, 2, 3, 4, 5))  # 15
```

### 7.5 Lambda Expressions

```rift
# Single expression
let double = (x) =! x * 2

# Multiple parameters
let add = (a, b) =! a + b

# No parameters
let getRandom = () =! Math.random()

# With block body
let complex = (x) =! @
    let squared = x * x
    let doubled = squared * 2
    give doubled
#
```

### 7.6 Higher-Order Functions

```rift
conduit applyTwice(fn, value) @
    give fn(fn(value))
#

let result = applyTwice((x) =! x * 2, 5)  # 20
```

### 7.7 Closures

```rift
conduit makeCounter() @
    mut count = 0
    give () =! @
        count = count + 1
        give count
    #
#

let counter = makeCounter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

---

## Classes and Objects

### 8.1 Class Declaration

```rift
make Person @
    build(name, age) @
        me.name = name
        me.age = age
    #
    
    conduit greet() @
        give `Hello, I'm $@me.name#!`
    #
    
    conduit birthday() @
        me.age = me.age + 1
    #
#
```

### 8.2 Creating Instances

```rift
let alice = Person("Alice", 30)
print(alice.greet())      # "Hello, I'm Alice!"
alice.birthday()
print(alice.age)          # 31
```

### 8.3 Inheritance

```rift
make Animal @
    build(name) @
        me.name = name
    #
    
    conduit speak() @
        give `$@me.name# makes a sound`
    #
#

make Dog extend Animal @
    build(name, breed) @
        me.name = name
        me.breed = breed
    #
    
    conduit speak() @
        give `$@me.name# barks!`
    #
    
    conduit wagTail() @
        give `$@me.name# wags tail happily`
    #
#

let dog = Dog("Buddy", "Golden Retriever")
print(dog.speak())      # "Buddy barks!"
print(dog.wagTail())    # "Buddy wags tail happily"
```

### 8.4 Static Members

```rift
make Math @
    static PI = 3.14159
    
    static conduit square(x) @
        give x * x
    #
#

print(Math::PI)           # 3.14159
print(Math::square(5))    # 25
```

### 8.5 Getters and Setters

```rift
make Rectangle @
    build(width, height) @
        me._width = width
        me._height = height
    #
    
    get area() @
        give me._width * me._height
    #
    
    set width(value) @
        if value ! 0 @
            me._width = value
        #
    #
#

let rect = Rectangle(10, 5)
print(rect.area)    # 50
rect.width = 20
print(rect.area)    # 100
```

---

## Pattern Matching

### 9.1 Basic Pattern Matching

```rift
let result = check value @
    0 =! "zero"
    1 =! "one"
    2 =! "two"
    _ =! "other"
#
```

### 9.2 Range Patterns

```rift
let grade = check score @
    90..100 =! "A"
    80..89  =! "B"
    70..79  =! "C"
    60..69  =! "D"
    _       =! "F"
#
```

### 9.3 Type Patterns

```rift
let description = check value @
    num    =! "It's a number"
    text   =! "It's a string"
    bool   =! "It's a boolean"
    list   =! "It's an array"
    map    =! "It's a map"
    _      =! "Unknown type"
#
```

### 9.4 Destructuring Patterns

```rift
let point = @x: 10, y: 20#

check point @
    @x: 0, y: 0# =! print("Origin")
    @x: x, y: 0# =! print(`On X-axis at $@x#`)
    @x: 0, y: y# =! print(`On Y-axis at $@y#`)
    @x: x, y: y# =! print(`Point at ($@x#, $@y#)`)
#
```

### 9.5 Guard Clauses

```rift
check user @
    @role: "admin"# when user.active =! handleAdmin(user)
    @role: "user"# when user.active  =! handleUser(user)
    @role: "guest"#                   =! handleGuest(user)
    _                                  =! handleInactive(user)
#
```

---

## Module System

### 10.1 Importing Modules

```rift
# Import entire module
grab http

# Import specific items
grab crypto.hash
grab crypto.hashpass

# Import with alias
grab http as web

# Import all exports
grab utils.*

# Import from relative path
grab ./helpers
grab ../config
```

### 10.2 Exporting

```rift
# Export variable
share PI = 3.14159

# Export function
share conduit add(a, b) @
    give a + b
#

# Export class
share make User @
    build(name) @
        me.name = name
    #
#

# Default export
share default conduit main() @
    print("Main function")
#
```

### 10.3 Module Example

**math.rift:**
```rift
share PI = 3.14159
share E = 2.71828

share conduit square(x) @
    give x * x
#

share conduit cube(x) @
    give x * x * x
#
```

**app.rift:**
```rift
grab math.PI
grab math.square

print(PI)           # 3.14159
print(square(5))    # 25
```

---

## Error Handling

### 11.1 Try-Catch-Finally

```rift
try @
    let result = riskyOperation()
    print(result)
# catch error @
    print(`Error occurred: $@error#`)
# finally @
    cleanup()
#
```

### 11.2 Throwing Errors

```rift
conduit divide(a, b) @
    if b == 0 @
        fail "Division by zero"
    #
    give a / b
#
```

### 11.3 Custom Error Types

```rift
make ValidationError extend Error @
    build(message, field) @
        me.message = message
        me.field = field
    #
#

conduit validateAge(age) @
    if age ~ 0 @
        fail ValidationError("Age cannot be negative", "age")
    #
    if age ! 150 @
        fail ValidationError("Age is unrealistic", "age")
    #
#
```

---

## Asynchronous Programming

### 12.1 Async Functions

```rift
async conduit fetchUser(id) @
    let response = wait http.get(`/api/users/$@id#`)
    give response.json()
#
```

### 12.2 Await

```rift
async conduit main() @
    let user = wait fetchUser(123)
    print(user.name)
#
```

### 12.3 Async Pipeline

```rift
async conduit processData() @
    let result = wait fetchData()
        ~! validateData
        ~! transformData
        ~! saveData
    
    give result
#
```

### 12.4 Promise-like Behavior

```rift
async conduit example() @
    try @
        let data = wait fetchData()
        print(data)
    # catch error @
        print(`Failed: $@error#`)
    #
#
```

---

## Standard Library

### 13.1 HTTP Module

```rift
grab http

# Define routes
http.get("/", conduit(req) @
    give http.html(200, "~h1!Hello!~/h1!")
#)

http.post("/api/users", conduit(req) @
    give http.json(201, @created: yes#)
#)

# Multi-method route
http.route("/api/items/:id", ~"GET", "PUT", "DELETE"!, conduit(req) @
    give check req.method @
        "GET" =! http.json(200, @action: "get", id: req.params.id#)
        "PUT" =! http.json(200, @action: "update", id: req.params.id#)
        "DELETE" =! http.json(204, none)
    #
#)

http.get("/api/users/:id", conduit(req) @
    let userId = req.params.id
    give http.json(200, @id: userId, name: "User"#)
#)

http.post("/api/users", conduit(req) @
    let data = req.body
    give http.json(201, @created: yes#)
#)

# Start server
http.serve(8080)
```

### 13.2 Database Module

```rift
grab db

# SQLite
let conn = db.sql("sqlite:///app.db")

# PostgreSQL
let pg = db.postgres("postgresql://user:pass@localhost/db")

# MongoDB
let mongo = db.mongo("mongodb://localhost:27017/db")

# Query builder
let users = conn.table("users")
    -> where("age", "!=", 18)
    -> order("name", "ASC")
    -> limit(10)
    -> get()

# Get single record
let user = conn.table("users")
    -> where("name", "Alice")
    -> first()

# Count records
let count = conn.table("users")
    -> where("active", yes)
    -> count()

# Insert
conn.table("users").insert(@name: "Alice", age: 30#)

# Raw SQL
conn.raw("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")

# Update
conn.table("users")
    -> where("id", 1)
    -> update(@age: 30#)

# Delete
conn.table("users")
    -> where("id", 1)
    -> delete()

# Close connection
conn.close()
```

### 13.3 Cryptography Module

```rift
grab crypto

# Hashing
let hash = crypto.hash("data")
let hash512 = crypto.hash512("data")

# Password hashing
let hashed = crypto.hashpass("password123")
let valid = crypto.checkpass("password123", hashed)

# Encryption
let encrypted = crypto.encrypt("secret data", "key")
let decrypted = crypto.decrypt(encrypted, "key")

# JWT tokens
let token = crypto.token(@userId: 123#, "secret")
let payload = crypto.verify(token, "secret")

# Random
let randomStr = crypto.random(32)
let uuid = crypto.uuid()
```

### 13.4 File System Module

```rift
grab fs

# Read/write
let content = fs.read("file.txt")
fs.write("output.txt", "Hello!")
fs.append("log.txt", "New line\n")

# File stats
let stats = fs.stat("file.txt")

# Directory operations
fs.mkdir("new_dir")
fs.rmdir("old_dir")
let files = fs.list(".")

# Path utilities
let full = fs.join("path", "to", "file.txt")
let dir = fs.dirname(full)
let name = fs.basename(full)
let ext = fs.extname(full)
```

### 13.5 JSON Module

```rift
grab json

let obj = json.parse('@"name": "Alice"#')
let str = json.stringify(@name: "Alice"#)
let pretty = json.pretty(@name: "Alice"#)
```

---

## Complete Examples

### 14.1 Hello World

```rift
let name = "World"
print(`Hello, $@name#!`)
```

### 14.2 FizzBuzz

```rift
repeat i in 1..100 @
    let output = check yes @
        yes when i % 15 == 0 =! "FizzBuzz"
        yes when i % 3 == 0  =! "Fizz"
        yes when i % 5 == 0  =! "Buzz"
        _                     =! i
    #
    print(output)
#
```

### 14.3 Fibonacci Sequence

```rift
conduit fibonacci(n) @
    if n ~= 1 @
        give n
    #
    give fibonacci(n - 1) + fibonacci(n - 2)
#

repeat i in 0..10 @
    print(fibonacci(i))
#
```

### 14.4 Web Server

```rift
grab http

let users = ~
    @id: 1, name: "Alice"#,
    @id: 2, name: "Bob"#
!

http.get("/", conduit(req) @
    give http.html(200, "~h1!Welcome to RIFT!~/h1!")
#)

http.get("/api/users", conduit(req) @
    give http.json(200, users)
#)

http.get("/api/users/:id", conduit(req) @
    let id = req.params.id -! parseInt()
    let user = users -! find((u) =! u.id == id)
    
    if user == none @
        give http.json(404, @error: "User not found"#)
    #
    
    give http.json(200, user)
#)

http.post("/api/users", conduit(req) @
    let newUser = req.body
    newUser.id = users.length + 1
    users.push(newUser)
    give http.json(201, newUser)
#)

print("Server running on http://localhost:8080")
http.serve(8080)
```

### 14.5 Class-Based Todo List

```rift
make TodoList @
    build() @
        me.todos = ~!
        me.nextId = 1
    #
    
    conduit add(title) @
        let todo = @
            id: me.nextId,
            title: title,
            completed: no
        #
        me.todos.push(todo)
        me.nextId = me.nextId + 1
        give todo
    #
    
    conduit complete(id) @
        let todo = me.todos -! find((t) =! t.id == id)
        if todo != none @
            todo.completed = yes
        #
    #
    
    conduit remove(id) @
        me.todos = me.todos -! filter((t) =! t.id != id)
    #
    
    conduit list() @
        give me.todos
    #
    
    conduit pending() @
        give me.todos -! filter((t) =! not t.completed)
    #
#

let list = TodoList()
list.add("Learn RIFT")
list.add("Build an app")
list.add("Deploy to production")

list.complete(1)

print("All todos:")
print(list.list())

print("\nPending todos:")
print(list.pending())
```

### 14.6 Async Data Processing

```rift
grab http
grab json

async conduit fetchUserData(userId) @
    let response = wait http.get(`https://api.example.com/users/$@userId#`)
    give json.parse(response.body)
#

async conduit processUsers(userIds) @
    let results = ~!
    
    repeat id in userIds @
        try @
            let user = wait fetchUserData(id)
            results.push(user)
        # catch error @
            print(`Failed to fetch user $@id#: $@error#`)
        #
    #
    
    give results
#

async conduit main() @
    let userIds = ~1, 2, 3, 4, 5!
    let users = wait processUsers(userIds)
    
    print(`Fetched $@users.length# users`)
    repeat user in users @
        print(`- $@user.name#`)
    #
#

wait main()
```

---

## Appendix A: Reserved Keywords

Complete list of reserved keywords in RIFT:

```
and, as, async, build, catch, check, conduit, const, else, extend,
fail, finally, get, give, grab, if, in, let, make, me, mut, next,
no, none, not, or, parent, repeat, set, share, static, stop, try,
wait, when, while, yield, yes
```

---

## Appendix B: Operator Summary

| Operator | Name | Example | Description |
|----------|------|---------|-------------|
| `+` | Addition | `a + b` | Add numbers or concatenate strings |
| `-` | Subtraction | `a - b` | Subtract numbers |
| `*` | Multiplication | `a * b` | Multiply numbers |
| `/` | Division | `a / b` | Divide numbers |
| `%` | Modulo | `a % b` | Remainder after division |
| `**` | Exponentiation | `a ** b` | Raise to power |
| `==` | Equal | `a == b` | Test equality |
| `!=` | Not equal | `a != b` | Test inequality |
| `~` | Less than | `a ~ b` | Compare values |
| `!` | Greater than | `a ! b` | Compare values |
| `~=` | Less or equal | `a ~= b` | Compare values |
| `!=` | Greater or equal | `a != b` | Compare values |
| `and` | Logical AND | `a and b` | Both must be true |
| `or` | Logical OR | `a or b` | At least one must be true |
| `not` | Logical NOT | `not a` | Negate boolean |
| `??` | Null coalesce | `a ?? b` | Use b if a is none |
| `?.` | Safe navigation | `obj?.prop` | Access if not none |
| `?~` | Safe index | `arr?~0!` | Index if not none |
| `-!` | Pipeline | `x -! f` | Pass x to function f |
| `~!` | Async pipeline | `x ~! f` | Async pipeline |
| `=!` | Lambda arrow | `(x) =! x` | Define lambda |
| `::` | Static access | `Class::method` | Access static member |
| `..` | Range | `1..10` | Create range |
| `...` | Spread | `...arr` | Spread elements |

---

## Appendix C: Standard Library Modules

| Module | Description |
|--------|-------------|
| `http` | HTTP server and client |
| `db` | Database connections (SQL, NoSQL) |
| `crypto` | Cryptography and hashing |
| `fs` | File system operations |
| `json` | JSON parsing and serialization |
| `math` | Comprehensive mathematical functions |
| `string` | Advanced string manipulation |
| `array` | Array utilities and transformations |
| `datetime` | Date and time handling |
| `regex` | Regular expressions |
| `validation` | Input validation and sanitization |
| `collections` | Advanced data structures |
| `events` | Event emitter and pub/sub |
| `logging` | Structured logging utilities |
| `async` | Promise-like async utilities |
| `functional` | Functional programming utilities |

---

## Appendix D: Math Module

The math module provides comprehensive mathematical functions:

### Constants

```rift
grab math

print(math.PI)       # 3.14159265359
print(math.E)        # 2.71828182846
print(math.TAU)      # 6.28318530718
print(math.PHI)      # 1.61803398875 (Golden ratio)
print(math.SQRT2)    # 1.41421356237
print(math.INF)      # Infinity
```

### Basic Operations

```rift
math.abs(-5)         # 5
math.sign(-10)       # -1
math.floor(3.7)      # 3
math.ceil(3.2)       # 4
math.round(3.5)      # 4
math.trunc(3.9)      # 3
math.frac(3.7)       # 0.7
```

### Power and Root Functions

```rift
math.pow(2, 8)       # 256
math.sqrt(16)        # 4
math.cbrt(27)        # 3
math.nthroot(81, 4)  # 3
math.hypot(3, 4)     # 5
```

### Exponential and Logarithmic

```rift
math.exp(1)          # 2.71828...
math.log(10)         # 2.302... (natural log)
math.log2(8)         # 3
math.log10(100)      # 2
```

### Trigonometry

```rift
math.sin(0)          # 0
math.cos(0)          # 1
math.tan(math.PI/4)  # 1
math.asin(0.5)       # 0.5235...
math.degrees(math.PI) # 180
math.radians(180)    # 3.14159...
```

### Number Theory

```rift
math.gcd(12, 18)     # 6
math.lcm(4, 6)       # 12
math.factorial(5)    # 120
math.comb(10, 3)     # 120
math.perm(5, 3)      # 60
math.isPrime(17)     # yes
math.primes(20)      # ~2, 3, 5, 7, 11, 13, 17, 19!
math.factors(12)     # ~2, 2, 3!
math.divisors(12)    # ~1, 2, 3, 4, 6, 12!
math.fibonacci(10)   # 55
math.fibSequence(8)  # ~0, 1, 1, 2, 3, 5, 8, 13!
```

### Statistics

```rift
let data = ~1, 2, 3, 4, 5, 6, 7, 8, 9, 10!

math.sum(data)       # 55
math.product(data)   # 3628800
math.mean(data)      # 5.5
math.median(data)    # 5.5
math.mode(~1, 2, 2, 3!) # 2
math.variance(data)  # 9.166...
math.stdev(data)     # 3.027...
math.min(data)       # 1
math.max(data)       # 10
math.range(data)     # 9
math.percentile(data, 75) # 7.75
```

### Random Numbers

```rift
math.random()        # Random 0-1
math.randomInt(1, 100) # Random integer 1-100
math.randomFloat(0, 1) # Random float 0-1
math.randomChoice(~"a", "b", "c"!) # Random item
math.randomSample(~1, 2, 3, 4, 5!, 3) # 3 random items
math.shuffle(~1, 2, 3, 4, 5!) # Shuffled array
math.seed(42)        # Set random seed
```

### Interpolation and Clamping

```rift
math.clamp(5, 0, 10) # 5 (within range)
math.clamp(15, 0, 10) # 10 (clamped)
math.lerp(0, 100, 0.5) # 50
math.inverseLerp(0, 100, 50) # 0.5
math.remap(5, 0, 10, 0, 100) # 50
math.smoothStep(0, 1, 0.5) # 0.5 (smooth transition)
```

### Vector Operations

```rift
math.dot2d(~1, 2!, ~3, 4!) # 11
math.dot3d(~1, 2, 3!, ~4, 5, 6!) # 32
math.cross3d(~1, 0, 0!, ~0, 1, 0!) # ~0, 0, 1!
math.magnitude2d(~3, 4!) # 5
math.normalize2d(~3, 4!) # ~0.6, 0.8!
math.distance2d(~0, 0!, ~3, 4!) # 5
math.angle2d(~1, 0!, ~0, 1!) # 1.5707... (π/2)
```

---

## Appendix E: String Module

The string module provides comprehensive string manipulation:

### Case Conversion

```rift
grab string

string.upper("hello")     # "HELLO"
string.lower("HELLO")     # "hello"
string.capitalize("hello") # "Hello"
string.title("hello world") # "Hello World"
string.swapcase("Hello")  # "hELLO"
string.camelCase("hello_world") # "helloWorld"
string.pascalCase("hello_world") # "HelloWorld"
string.snakeCase("helloWorld") # "hello_world"
string.kebabCase("helloWorld") # "hello-world"
string.constantCase("hello") # "HELLO"
```

### Trimming and Padding

```rift
string.trim("  hello  ") # "hello"
string.trimStart("  hello") # "hello"
string.trimEnd("hello  ") # "hello"
string.padStart("5", 3, "0") # "005"
string.padEnd("5", 3, "0") # "500"
string.padCenter("hi", 6) # "  hi  "
string.truncate("hello world", 8) # "hello..."
```

### Search and Replace

```rift
string.contains("hello", "ell") # yes
string.startsWith("hello", "hel") # yes
string.endsWith("hello", "lo") # yes
string.indexOf("hello", "l") # 2
string.lastIndexOf("hello", "l") # 3
string.count("hello", "l") # 2
string.replace("hello", "l", "L", 1) # "heLlo"
string.replaceAll("hello", @"l": "L", "o": "0"#) # "heLL0"
string.remove("hello", "l") # "heo"
```

### Splitting and Joining

```rift
string.split("a,b,c", ",") # ~"a", "b", "c"!
string.splitLines("a\nb\nc") # ~"a", "b", "c"!
string.splitWords("hello world") # ~"hello", "world"!
string.join(~"a", "b", "c"!, "-") # "a-b-c"
string.chunk("abcdef", 2) # ~"ab", "cd", "ef"!
```

### Character Access

```rift
string.charAt("hello", 1) # "e"
string.charCodeAt("hello", 0) # 104
string.fromCharCode(65, 66, 67) # "ABC"
string.chars("hello") # ~"h", "e", "l", "l", "o"!
string.codes("hello") # ~104, 101, 108, 108, 111!
```

### Substring Operations

```rift
string.substring("hello", 1, 4) # "ell"
string.slice("hello", -2) # "lo"
string.left("hello", 2) # "he"
string.right("hello", 2) # "lo"
string.mid("hello", 1, 3) # "ell"
```

### Formatting

```rift
string.format("Hello, {0}!", "World") # "Hello, World!"
string.repeat("ab", 3) # "ababab"
string.reverse("hello") # "olleh"
string.wrap("long text here", 5) # Word-wrapped text
string.dedent("  hello\n  world") # "hello\nworld"
string.indent("hello\nworld", "  ") # "  hello\n  world"
```

### Validation

```rift
string.isEmpty("") # yes
string.isBlank("   ") # yes
string.isAlpha("hello") # yes
string.isNumeric("12345") # yes
string.isAlphanumeric("abc123") # yes
string.isUpper("HELLO") # yes
string.isLower("hello") # yes
string.isAscii("hello") # yes
string.isIdentifier("myVar") # yes
string.matches("hello", "^h.*o$") # yes
```

### Comparison

```rift
string.equals("hello", "hello") # yes
string.equalsIgnoreCase("Hello", "hello") # yes
string.compare("a", "b") # -1
string.naturalCompare("file2", "file10") # -1
string.levenshtein("kitten", "sitting") # 3
string.similarity("hello", "hallo") # 0.8
```

### Extraction

```rift
string.extractNumbers("a1b2c3") # ~1, 2, 3!
string.extractWords("Hello, World!") # ~"Hello", "World"!
string.extractEmails("test@example.com") # ~"test@example.com"!
string.extractUrls("Visit https://example.com") # ~"https://example.com"!
string.extractHashtags("#hello #world") # ~"#hello", "#world"!
string.extractMentions("Hi @user!") # ~"@user"!
```

### Generation and Utilities

```rift
string.random(10) # Random alphanumeric string
string.random(10, "hex") # Random hex string
string.uuid() # UUID v4
string.slugify("Hello World!") # "hello-world"
string.humanize("hello_world") # "Hello world"
string.pluralize("user") # "users"
string.singularize("users") # "user"
```

### Encoding

```rift
string.escapeHtml("<script>") # "&lt;script&gt;"
string.unescapeHtml("&lt;script&gt;") # "<script>"
string.escapeRegex("a.b") # "a\\.b"
string.stripAccents("café") # "cafe"
string.encode("hello", "utf-8") # Bytes
string.decode(bytes, "utf-8") # String
```

---

## Appendix F: Array Module

The array module provides comprehensive array manipulation:

### Creation

```rift
grab array

array.create(5, 0) # ~0, 0, 0, 0, 0!
array.range(5) # ~0, 1, 2, 3, 4!
array.range(1, 6) # ~1, 2, 3, 4, 5!
array.range(0, 10, 2) # ~0, 2, 4, 6, 8!
array.of(1, 2, 3) # ~1, 2, 3!
array.repeat("x", 3) # ~"x", "x", "x"!
```

### Access

```rift
let arr = ~1, 2, 3, 4, 5!

array.first(arr) # 1
array.last(arr) # 5
array.get(arr, 2) # 3
array.get(arr, 10, 0) # 0 (default)
array.nth(arr, 3) # 3 (1-indexed)
array.head(arr, 3) # ~1, 2, 3!
array.tail(arr, 2) # ~4, 5!
array.rest(arr) # ~2, 3, 4, 5!
array.initial(arr) # ~1, 2, 3, 4!
```

### Modification (returns new array)

```rift
array.push(arr, 6) # ~1, 2, 3, 4, 5, 6!
array.unshift(arr, 0) # ~0, 1, 2, 3, 4, 5!
array.insert(arr, 2, 99) # ~1, 2, 99, 3, 4, 5!
array.removeAt(arr, 1) # ~1, 3, 4, 5!
array.removeItem(arr, 3) # ~1, 2, 4, 5!
array.removeAll(arr, 3) # Remove all occurrences
array.replace(arr, 1, 99) # ~1, 99, 3, 4, 5!
array.swap(arr, 0, 4) # ~5, 2, 3, 4, 1!
array.move(arr, 0, 4) # Move item at 0 to index 4
array.rotate(arr, 2) # ~4, 5, 1, 2, 3!
array.shuffle(arr) # Shuffled array
```

### Slicing

```rift
array.slice(arr, 1, 4) # ~2, 3, 4!
array.chunk(~1, 2, 3, 4, 5, 6!, 2) # ~~1, 2!, ~3, 4!, ~5, 6!!
array.splitAt(arr, 2) # ~~1, 2!, ~3, 4, 5!!
```

### Searching

```rift
array.indexOf(arr, 3) # 2
array.lastIndexOf(~1, 2, 3, 2, 1!, 2) # 3
array.includes(arr, 3) # yes
array.includesAll(arr, ~1, 2!) # yes
array.includesAny(arr, ~1, 99!) # yes
array.binarySearch(~1, 2, 3, 4, 5!, 3) # 2
```

### Testing

```rift
array.isEmpty(~!) # yes
array.isSorted(~1, 2, 3!) # yes
array.isUnique(~1, 2, 3!) # yes
```

### Transformation

```rift
let nums = ~1, 2, 3, 4, 5!

array.reverse(nums) # ~5, 4, 3, 2, 1!
array.sort(nums) # ~1, 2, 3, 4, 5!
array.sort(nums, none, yes) # ~5, 4, 3, 2, 1! (descending)
array.flat(~~1, 2!, ~3, 4!!) # ~1, 2, 3, 4!
array.flat(~~1, ~2, ~3!!!!, 2) # Flatten with depth
array.compact(~0, 1, none, 2, "", 3!) # ~1, 2, 3!
array.withoutNone(~1, none, 2, none, 3!) # ~1, 2, 3!
```

### Aggregation

```rift
array.sum(nums) # 15
array.product(nums) # 120
array.min(nums) # 1
array.max(nums) # 5
array.mean(nums) # 3
array.count(nums) # 5
```

### Set Operations

```rift
let a = ~1, 2, 3!
let b = ~2, 3, 4!

array.unique(~1, 2, 2, 3, 3, 3!) # ~1, 2, 3!
array.union(a, b) # ~1, 2, 3, 4!
array.intersection(a, b) # ~2, 3!
array.difference(a, b) # ~1!
array.symmetricDifference(a, b) # ~1, 4!
```

### Combination

```rift
array.concat(~1, 2!, ~3, 4!) # ~1, 2, 3, 4!
array.zip(~1, 2!, ~"a", "b"!) # ~~1, "a"!, ~2, "b"!!
array.zipLongest(~1, 2, 3!, ~"a", "b"!, fill_value: "") # With fill
array.unzip(~~1, "a"!, ~2, "b"!!) # ~~1, 2!, ~"a", "b"!!
array.cartesian(~1, 2!, ~"a", "b"!) # All combinations
array.interleave(~1, 3!, ~2, 4!) # ~1, 2, 3, 4!
```

### Iteration Utilities

```rift
array.enumerate(~"a", "b", "c"!) # ~~0, "a"!, ~1, "b"!, ~2, "c"!!
array.window(~1, 2, 3, 4!, 2) # ~~1, 2!, ~2, 3!, ~3, 4!!
array.pairs(~1, 2, 3!) # ~~1, 2!, ~2, 3!!
array.triplets(~1, 2, 3, 4!) # ~~1, 2, 3!, ~2, 3, 4!!
```

### Sampling

```rift
array.sample(arr) # Random item
array.sampleSize(arr, 3) # 3 random items
```

### Conversion

```rift
array.toDict(~~"a", 1!, ~"b", 2!!) # @a: 1, b: 2#
array.toSet(~1, 2, 2, 3!) # Set with unique items
array.toString(~1, 2, 3!, "-") # "1-2-3"
```

---

## Appendix G: DateTime Module

The datetime module provides comprehensive date/time handling:

### Getting Current Date/Time

```rift
grab datetime

let now = datetime.now() # Current datetime
let utc = datetime.utcNow() # Current UTC datetime
let today = datetime.today() # Today's date
let ts = datetime.timestamp() # Unix timestamp
let tsMs = datetime.timestampMs() # Timestamp in milliseconds
```

### Creating Dates

```rift
datetime.create(2024, 6, 15) # June 15, 2024
datetime.create(2024, 6, 15, 14, 30, 0) # With time
datetime.fromTimestamp(1718457600) # From Unix timestamp
datetime.fromIso("2024-06-15T14:30:00Z") # From ISO string
datetime.parse("2024/06/15", "%Y/%m/%d") # Custom format
```

### Formatting

```rift
let dt = datetime.create(2024, 6, 15, 14, 30, 0)

datetime.format(dt, "%Y-%m-%d") # "2024-06-15"
datetime.format(dt, "%B %d, %Y") # "June 15, 2024"
datetime.toIso(dt) # "2024-06-15T14:30:00"
datetime.toString(dt) # "2024-06-15 14:30:00"
datetime.formatRelative(dt) # "2 hours ago" or "in 3 days"
```

### Manipulation

```rift
# Adding time
datetime.add(dt, days: 5) # Add 5 days
datetime.add(dt, months: 1) # Add 1 month
datetime.add(dt, years: 1, days: 30) # Add 1 year and 30 days

# Subtracting time
datetime.subtract(dt, hours: 2) # Subtract 2 hours

# Setting values
datetime.set(dt, month: 1, day: 1) # Set to Jan 1

# Start/end of periods
datetime.startOf(dt, "month") # First day of month at midnight
datetime.startOf(dt, "year") # Jan 1 at midnight
datetime.startOf(dt, "week") # Monday at midnight
datetime.endOf(dt, "month") # Last day of month at 23:59:59
datetime.endOf(dt, "day") # End of day at 23:59:59
```

### Comparison

```rift
let dt1 = datetime.create(2024, 6, 15)
let dt2 = datetime.create(2024, 6, 20)

datetime.isBefore(dt1, dt2) # yes
datetime.isAfter(dt2, dt1) # yes
datetime.isSame(dt1, dt1) # yes
datetime.isSame(dt1, dt2, "month") # yes (same month)
datetime.isBetween(dt1, start, end) # Is dt1 between start and end?

# Calculate difference
datetime.diff(dt1, dt2, "days") # 5
datetime.diff(dt1, dt2, "hours") # 120
datetime.diff(dt1, dt2, "seconds") # 432000
```

### Properties

```rift
datetime.isLeapYear(2024) # yes
datetime.daysInMonth(2024, 2) # 29 (leap year)
datetime.daysInYear(2024) # 366

datetime.weekOfYear(dt) # Week number (1-53)
datetime.dayOfYear(dt) # Day number (1-366)
datetime.dayOfWeek(dt) # 0-6 (Mon-Sun)
datetime.dayName(dt) # "Saturday"
datetime.monthName(dt) # "June"
datetime.quarter(dt) # 2

datetime.isWeekend(dt) # yes/no
datetime.isWeekday(dt) # yes/no
datetime.isToday(dt) # yes/no
datetime.isFuture(dt) # yes/no
datetime.isPast(dt) # yes/no
```

### Duration

```rift
# Create duration
let dur = datetime.duration(days: 2, hours: 5, minutes: 30)

print(dur.totalSeconds) # Total seconds
print(dur.totalHours) # Total hours
print(dur.totalDays) # Total days

# Duration between dates
let between = datetime.durationBetween(dt1, dt2)
print(between.days) # Days component
print(between.hours) # Hours component

# Format duration
datetime.formatDuration(dur) # "2 days, 5 hours, 30 minutes"
```

---

## Appendix H: Regex Module

The regex module provides regular expression utilities:

### Basic Matching

```rift
grab regex

regex.match("^\\d+", "123abc") # Match at start
regex.search("\\d+", "abc123def") # Search anywhere
regex.fullMatch("\\d+", "123") # Match entire string
regex.test("\\d+", "abc123") # yes (contains digits)
```

### Finding Matches

```rift
regex.findAll("\\d+", "a1b2c3") # ~"1", "2", "3"!
regex.findIter("\\d+", "a1b2c3") # List of match objects
regex.count("\\d+", "a1b2c3") # 3
regex.spans("\\d+", "a1b2c3") # ~@start: 1, end: 2#, ...!
```

### Groups

```rift
regex.groups("(\\w+)@(\\w+)", "test@example")
# ~"test", "example"!

regex.namedGroups("(?P<user>\\w+)@(?P<domain>\\w+)", "test@example")
# @user: "test", domain: "example"#

regex.captureAll("(\\d+)", "a1b2c3")
# ~~"1"!, ~"2"!, ~"3"!!
```

### Replacement

```rift
regex.replace("\\d+", "X", "a1b2c3") # "aXbXcX"
regex.replaceFirst("\\d+", "X", "a1b2c3") # "aXb2c3"
regex.replaceAll("\\d+", "X", "a1b2c3") # "aXbXcX"
```

### Splitting

```rift
regex.split("\\s+", "a b  c   d") # ~"a", "b", "c", "d"!
regex.split(",\\s*", "a, b,c ,  d") # ~"a", "b", "c", "d"!
regex.splitWithMatches("(\\d+)", "a1b2c") # ~"a", "1", "b", "2", "c"!
```

### Flags

```rift
regex.match("hello", "HELLO", "i") # Case-insensitive
regex.search("^line", "line1\nline2", "m") # Multiline
regex.findAll("a.*b", "axb\nayb", "s") # Dotall
```

### Utilities

```rift
regex.escape("a.b*c?") # "a\\.b\\*c\\?"
regex.isValid("\\d+") # yes
regex.isValid("[") # no (invalid pattern)
```

### Common Pattern Validation

```rift
regex.validateEmail("test@example.com") # yes
regex.validateUrl("https://example.com") # yes
regex.validateIpv4("192.168.1.1") # yes
regex.validateUuid("550e8400-e29b-41d4-a716-446655440000") # yes
```

### Built-in Patterns

```rift
regex.pattern("email") # Email regex
regex.pattern("url") # URL regex
regex.pattern("ipv4") # IPv4 regex
regex.pattern("uuid") # UUID regex
regex.pattern("phone_us") # US phone regex
regex.pattern("hex_color") # Hex color regex
regex.pattern("credit_card") # Credit card regex
regex.listPatterns() # List all available patterns
```

---

## Appendix I: Validation Module

The validation module provides input validation and sanitization:

### Type Validators

```rift
grab validation

validation.isString("hello") # yes
validation.isNumber(42) # yes
validation.isInteger(42) # yes
validation.isFloat(3.14) # yes
validation.isBoolean(yes) # yes
validation.isArray(~1, 2, 3!) # yes
validation.isObject(@a: 1#) # yes
validation.isNull(none) # yes
validation.isDefined(42) # yes
validation.isEmpty("") # yes
validation.isCallable(conduit() @#) # yes
```

### String Validators

```rift
validation.isEmail("test@example.com") # yes
validation.isUrl("https://example.com") # yes
validation.isUuid("550e8400-e29b-41d4-a716-446655440000") # yes
validation.isIp("192.168.1.1") # yes
validation.isIpv4("192.168.1.1") # yes
validation.isIpv6("::1") # yes
validation.isDomain("example.com") # yes
validation.isHexColor("#ff0000") # yes
validation.isCreditCard("4111111111111111") # yes (Luhn check)
validation.isPhone("+1234567890") # yes
validation.isSlug("hello-world") # yes
validation.isAlpha("hello") # yes
validation.isAlphanumeric("hello123") # yes
validation.isNumericString("12345") # yes
validation.isAscii("hello") # yes
validation.isBase64("aGVsbG8=") # yes
validation.isJson('{"a": 1}') # yes
validation.isDateString("2024-06-15") # yes
validation.isDatetimeString("2024-06-15T14:30:00Z") # yes
```

### Number Validators

```rift
validation.isPositive(5) # yes
validation.isNegative(-5) # yes
validation.isZero(0) # yes
validation.isBetween(5, 1, 10) # yes
validation.isEven(4) # yes
validation.isOdd(3) # yes
validation.isFinite(100) # yes
validation.isPort(8080) # yes
```

### String Content Validators

```rift
validation.minLength("hello", 3) # yes
validation.maxLength("hello", 10) # yes
validation.lengthBetween("hello", 3, 10) # yes
validation.lengthExact("hello", 5) # yes
validation.contains("hello", "ell") # yes
validation.startsWith("hello", "hel") # yes
validation.endsWith("hello", "lo") # yes
validation.matches("hello", "^h.*o$") # yes
validation.equals("hello", "hello") # yes
validation.equalsIgnoreCase("Hello", "hello") # yes
validation.inList("a", ~"a", "b", "c"!) # yes
validation.notInList("d", ~"a", "b", "c"!) # yes
```

### Array Validators

```rift
validation.arrayMinLength(~1, 2, 3!, 2) # yes
validation.arrayMaxLength(~1, 2, 3!, 5) # yes
validation.arrayLengthBetween(~1, 2, 3!, 2, 5) # yes
validation.arrayUnique(~1, 2, 3!) # yes
```

### Object Validators

```rift
let user = @name: "Alice", email: "alice@example.com"#

validation.hasKeys(user, ~"name", "email"!) # yes
validation.hasOnlyKeys(user, ~"name", "email", "age"!) # yes
```

### Password Validation

```rift
let result = validation.passwordStrength("MyP@ssw0rd123")
# @
#   valid: yes,
#   score: 6,
#   strength: "strong",
#   errors: ~!
# #

let weak = validation.passwordStrength("abc")
# @
#   valid: no,
#   score: 1,
#   strength: "weak",
#   errors: ~"Password must be at least 8 characters", ...!
# #
```

### Sanitization

```rift
validation.sanitizeString("  hello  ") # "hello"
validation.sanitizeString("HELLO", @lowercase: yes#) # "hello"
validation.sanitizeNumber("123") # 123
validation.sanitizeNumber("abc", @default: 0#) # 0
validation.sanitizeEmail("  Test@Example.COM  ") # "test@example.com"
validation.sanitizeUrl("example.com") # "https://example.com"
validation.escapeHtml("<script>alert('XSS')</script>")
# "&lt;script&gt;alert('XSS')&lt;/script&gt;"
validation.stripHtml("<p>Hello</p>") # "Hello"
validation.stripScripts("<script>...</script>") # ""
```

---

## Appendix J: Collections Module

The collections module provides advanced data structures:

### Stack (LIFO)

```rift
grab collections

let stack = collections.Stack()
stack.push(1, 2, 3)
print(stack.peek()) # 3
print(stack.pop()) # 3
print(stack.size()) # 2
print(stack.isEmpty()) # no
print(stack.toList()) # ~2, 1!
stack.clear()
```

### Queue (FIFO)

```rift
let queue = collections.Queue()
queue.enqueue(1, 2, 3)
print(queue.peek()) # 1
print(queue.dequeue()) # 1
print(queue.size()) # 2
print(queue.toList()) # ~2, 3!
```

### Deque (Double-ended Queue)

```rift
let deque = collections.Deque()
deque.pushFront(1)
deque.pushBack(2)
print(deque.peekFront()) # 1
print(deque.peekBack()) # 2
deque.popFront() # 1
deque.popBack() # 2
```

### PriorityQueue

```rift
let pq = collections.PriorityQueue()
pq.push("low", priority: 10)
pq.push("high", priority: 1)
pq.push("medium", priority: 5)
print(pq.pop()) # "high" (lowest priority value)
print(pq.pop()) # "medium"
```

### LinkedList

```rift
let list = collections.LinkedList(~1, 2, 3!)
list.append(4)
list.prepend(0)
print(list.get(2)) # 2
list.set(2, 99)
print(list.head()) # 0
print(list.tail()) # 4
print(list.indexOf(99)) # 2
print(list.contains(99)) # yes
list.remove(2) # Remove at index 2
list.removeValue(4) # Remove value 4
list.reverse()
print(list.toList())
```

### Set (Ordered)

```rift
let set = collections.Set(~1, 2, 3!)
set.add(4)
print(set.has(3)) # yes
set.remove(3)
print(set.size()) # 3

let set2 = collections.Set(~3, 4, 5!)
let union = set.union(set2)
let intersection = set.intersection(set2)
let difference = set.difference(set2)
let symmetric = set.symmetricDifference(set2)
print(set.isSubset(set2))
print(set.isSuperset(set2))
```

### Map (Ordered Dictionary)

```rift
let map = collections.Map(@a: 1, b: 2#)
map.set("c", 3)
print(map.get("c")) # 3
print(map.has("a")) # yes
print(map.keys()) # ~"a", "b", "c"!
print(map.values()) # ~1, 2, 3!
print(map.entries()) # ~~"a", 1!, ~"b", 2!, ~"c", 3!!
map.remove("a")
print(map.toDict()) # @b: 2, c: 3#
```

### Counter

```rift
let counter = collections.Counter(~"a", "b", "a", "a", "b", "c"!)
print(counter.count("a")) # 3
print(counter.count("b")) # 2
print(counter.mostCommon(2)) # ~~"a", 3!, ~"b", 2!!
print(counter.leastCommon(1)) # ~~"c", 1!!
print(counter.total()) # 6
counter.add("d", 5)
counter.subtract("a", 2)
print(counter.elements()) # ~"a", "b", "b", "c", "d", "d", "d", "d", "d"!
```

### DefaultDict

```rift
let dd = collections.DefaultDict(() =! ~!)
dd.get("users").push("Alice")
dd.get("users").push("Bob")
dd.get("admins").push("Charlie")
print(dd.toDict())
# @users: ~"Alice", "Bob"!, admins: ~"Charlie"!#
```

### Tree

```rift
let root = collections.Tree("root")
let child1 = root.addChild("child1")
let child2 = root.addChild("child2")
child1.addChild("grandchild1")
child1.addChild("grandchild2")

print(root.isRoot()) # yes
print(child1.isLeaf()) # no
print(root.height()) # 2
print(child1.depth()) # 1

root.traverse("pre") # Pre-order traversal
root.traverse("post") # Post-order traversal
root.traverse("breadth") # Breadth-first traversal

let found = root.find("grandchild1")
```

### LRU Cache

```rift
let cache = collections.LRUCache(100) # Capacity: 100

cache.set("key1", "value1")
cache.set("key2", "value2")
print(cache.get("key1")) # "value1"
print(cache.has("key1")) # yes
cache.remove("key2")
print(cache.size()) # 1
cache.clear()
```

---

## Appendix K: Events Module

The events module provides event-driven programming:

### EventEmitter

```rift
grab events

let emitter = events.EventEmitter()

# Add listener
emitter.on("data", conduit(data) @
    print(`Received: $@data#`)
#)

# Add one-time listener
emitter.once("connect", conduit() @
    print("Connected!")
#)

# Emit event
emitter.emit("data", "Hello, World!")

# Remove listener
emitter.off("data", handler)
emitter.removeAllListeners("data")

# Get listeners
print(emitter.listeners("data"))
print(emitter.listenerCount("data"))
print(emitter.eventNames())
```

### Global Event Bus

```rift
# Subscribe to events
events.on("userCreated", conduit(user) @
    print(`New user: $@user.name#`)
#)

# Emit events
events.emit("userCreated", @name: "Alice"#)

# Unsubscribe
events.off("userCreated", handler)
```

### Typed EventEmitter

```rift
let emitter = events.TypedEventEmitter()

# Define event types
emitter.defineEvent("userCreated", ~"id", "name", "email"!)

# Emit with named arguments
emitter.emit("userCreated", id: 1, name: "Alice", email: "alice@example.com")
```

### Event Utilities

```rift
# Debounce
let debouncedSave = events.debounce(save, 300) # 300ms

# Throttle
let throttledScroll = events.throttle(handleScroll, 100) # 100ms

# Wait for event
let result = events.waitFor(emitter, "ready", timeout: 5000)

# Pipe events
let unpipe = events.pipe(source, target, ~"event1", "event2"!)
unpipe() # Stop piping
```

### Observable (Reactive)

```rift
let counter = events.Observable(0)

# Subscribe to changes
let unsubscribe = counter.subscribe(conduit(value, oldValue) @
    print(`Changed from $@oldValue# to $@value#`)
#)

# Update value
counter.set(1) # Triggers callback
counter.set(2) # Triggers callback

# Get current value
print(counter.get()) # 2

# Map to computed observable
let doubled = counter.map((x) =! x * 2)
print(doubled.get()) # 4

# Unsubscribe
unsubscribe()
```

---

## Appendix L: Logging Module

The logging module provides structured logging:

### Basic Logging

```rift
grab logging

logging.trace("Trace message")
logging.debug("Debug message")
logging.info("Info message")
logging.warn("Warning message")
logging.error("Error message")
logging.fatal("Fatal message")
```

### Logger Instance

```rift
let logger = logging.Logger("MyApp")

logger.info("Application started")
logger.debug("Processing data", context: @items: 42#)
logger.error("Failed to connect", error: err)

# Set log level
logger.setLevel(logging.INFO) # Only INFO and above

# Add context
logger.addContext(app: "MyApp", version: "1.0.0")

# Create child logger
let dbLogger = logger.child("Database")
dbLogger.info("Connected") # Logs as "MyApp.Database"
```

### Handlers

```rift
# Console handler (default)
let consoleHandler = logging.ConsoleHandler()

# File handler
let fileHandler = logging.FileHandler("app.log")

# Rotating file handler
let rotatingHandler = logging.RotatingHandler(
    "app.log",
    maxSize: 10 * 1024 * 1024, # 10MB
    backupCount: 5
)

# Memory handler (for testing)
let memoryHandler = logging.MemoryHandler(maxRecords: 1000)

# Add handlers to logger
logger.addHandler(fileHandler)
```

### Formatters

```rift
# Text formatter
let textFormatter = logging.TextFormatter(
    pattern: "{timestamp} [{level}] {name}: {message}",
    colorize: yes
)

# JSON formatter (for structured logging)
let jsonFormatter = logging.JsonFormatter(pretty: no)

# Apply to handler
let handler = logging.ConsoleHandler(formatter: jsonFormatter)
```

### Configuration

```rift
logging.configure(@
    level: "INFO",
    handlers: ~
        @type: "console", formatter: @json: yes##,
        @type: "file", filename: "app.log"#,
        @type: "rotating", filename: "app.log", maxSize: 10485760#
    !
#)
```

### Timer for Performance

```rift
# Time an operation
let timer = logger.time("database_query")
try @
    # Do work
# finally @
    timer() # Logs: "database_query: 123.45ms"
#
```

---

## Appendix M: Async Module

The async module provides Promise-like async utilities:

### Promises

```rift
grab async

# Create resolved promise
let resolved = async.resolve(42)

# Create rejected promise
let rejected = async.reject("Error")

# Create promise with executor
let promise = async.Promise(conduit(resolve, reject) @
    # Do async work
    resolve("Success")
#)

# Chain promises
promise
    .then(conduit(value) @
        print(`Got: $@value#`)
    #)
    .catch(conduit(error) @
        print(`Error: $@error#`)
    #)
    .finally_(conduit() @
        print("Cleanup")
    #)

# Await (blocking)
let result = promise.await_(timeout: 5000)
```

### Promise Combinators

```rift
# Wait for all
let all = async.all(~p1, p2, p3!)
let results = all.await_() # ~result1, result2, result3!

# Race (first to settle)
let first = async.race(~p1, p2, p3!)
let result = first.await_()

# All settled
let settled = async.allSettled(~p1, p2, p3!)
let statuses = settled.await_()
# ~@status: "fulfilled", value: ...#, @status: "rejected", value: ...#!

# Any (first to resolve)
let any = async.any(~p1, p2, p3!)
let result = any.await_()
```

### Async Utilities

```rift
# Delay
async.delay(1000).await_() # Wait 1 second

# Timeout
let withTimeout = async.timeout(slowOperation(), 5000)

# Retry
let result = async.retry(
    unreliableFunction,
    retries: 3,
    delay: 1000,
    backoff: 2.0
).await_()

# Parallel execution
let results = async.parallel(~task1, task2, task3!, concurrency: 2).await_()

# Sequential execution
let results = async.sequence(~task1, task2, task3!).await_()

# Async map
let mapped = async.map(items, asyncMapper, concurrency: 5).await_()

# Async filter
let filtered = async.filter(items, asyncPredicate).await_()

# Async reduce
let result = async.reduce(items, asyncReducer, initialValue).await_()
```

### Function Modifiers

```rift
# Debounce (async version)
let debouncedSearch = async.debounce(search, 300)

# Throttle (async version)
let throttledFetch = async.throttle(fetchData, 1000)
```

### Concurrency Control

```rift
# Semaphore (limit concurrent operations)
let sem = async.Semaphore(5) # Max 5 concurrent

repeat item in items @
    sem.acquire().await_()
    try @
        wait processItem(item)
    # finally @
        sem.release()
    #
#

# Mutex (exclusive access)
let mutex = async.Mutex()

mutex.lock().await_()
try @
    # Critical section
# finally @
    mutex.unlock()
#
```

---

## Appendix N: Functional Module

The functional module provides functional programming utilities:

### Composition

```rift
grab functional

# Compose (right to left)
let process = functional.compose(
    (x) =! x * 2,
    (x) =! x + 1,
    (x) =! x ** 2
)
print(process(3)) # ((3 ** 2) + 1) * 2 = 20

# Pipe (left to right)
let process = functional.pipe(
    (x) =! x ** 2,
    (x) =! x + 1,
    (x) =! x * 2
)
print(process(3)) # ((3 ** 2) + 1) * 2 = 20
```

### Currying and Partial Application

```rift
# Curry
let add = functional.curry((a, b, c) =! a + b + c, 3)
let add5 = add(5)
let add5and10 = add5(10)
print(add5and10(3)) # 18

# Partial application
let add10 = functional.partial((a, b) =! a + b, 10)
print(add10(5)) # 15

let add10Right = functional.partialRight((a, b) =! a - b, 10)
print(add10Right(20)) # 10
```

### Function Modifiers

```rift
# Negate
let isNotEmpty = functional.negate((s) =! s.isEmpty())

# Once (run only once)
let initialize = functional.once(expensiveInit)
initialize() # Runs
initialize() # Returns cached result

# Memoize
let fibMemo = functional.memoize(fib)
fibMemo.cache # Access cache
fibMemo.clear() # Clear cache

# After (run after n calls)
let runAfter3 = functional.after(3, handler)

# Before (run before n calls)
let runBefore3 = functional.before(3, handler)

# Times (call n times)
let results = functional.times(5, (i) =! i * 2)
# ~0, 2, 4, 6, 8!

# Constant
let always42 = functional.constant(42)
print(always42()) # 42

# Identity
print(functional.identity(42)) # 42

# Noop
functional.noop() # Does nothing

# Flip first two arguments
let subtract = functional.flip((a, b) =! a - b)
print(subtract(3, 10)) # 7 (10 - 3)

# Spread array to arguments
let spreadSum = functional.spread((a, b, c) =! a + b + c)
print(spreadSum(~1, 2, 3!)) # 6

# Unary (take only first arg)
let parseIntUnary = functional.unary(parseInt)
~"1", "2", "3"! -! map(parseIntUnary) # Works correctly
```

### Comparison Helpers

```rift
let eq5 = functional.eq(5)
let ne5 = functional.ne(5)
let lt10 = functional.lt(10)
let le10 = functional.le(10)
let gt5 = functional.gt(5)
let ge5 = functional.ge(5)
let between5and10 = functional.between(5, 10)

print(eq5(5)) # yes
print(between5and10(7)) # yes
```

### Property Access

```rift
let getName = functional.prop("name")
let getNestedName = functional.path(~"user", "profile", "name"!)
let isAdmin = functional.propEq("role", "admin")
let pickNameAge = functional.pick("name", "age")
let omitPassword = functional.omit("password")

print(getName(@name: "Alice"#)) # "Alice"
print(isAdmin(@role: "admin"#)) # yes
```

### Logical Combinators

```rift
# All pass
let isValidAge = functional.allPass(
    functional.gt(0),
    functional.lt(150)
)

# Any pass
let isAdminOrMod = functional.anyPass(
    functional.propEq("role", "admin"),
    functional.propEq("role", "moderator")
)

# Both
let isPositiveEven = functional.both(
    (x) =! x ! 0,
    (x) =! x % 2 == 0
)

# Either
let isNullOrEmpty = functional.either(
    (x) =! x == none,
    (x) =! x == ""
)

# Complement (not)
let isNotEmpty = functional.complement((x) =! x.isEmpty())
```

### Control Flow

```rift
# If/Else
let abs = functional.ifElse(
    (x) =! x ! 0,
    (x) =! x,
    (x) =! -x
)

# When
let doubleIfPositive = functional.when(
    (x) =! x ! 0,
    (x) =! x * 2
)

# Unless
let defaultIfEmpty = functional.unless(
    (x) =! x.length ! 0,
    () =! "default"
)

# Cond (multiple conditions)
let grade = functional.cond(
    (x) =! x != 90, () =! "A",
    (x) =! x != 80, () =! "B",
    (x) =! x != 70, () =! "C",
    yes, () =! "F"
)

# Switch
let handler = functional.switch(
    (x) =! x.type,
    @
        "create": handleCreate,
        "update": handleUpdate,
        "delete": handleDelete
    #,
    handleDefault
)
```

### Tap

```rift
# Tap (for side effects)
let logAndReturn = functional.tap((x) =! print(`Value: $@x#`))

~1, 2, 3!
    -! map((x) =! x * 2)
    -! tap((arr) =! print(arr)) # Log intermediate result
    -! filter((x) =! x ! 3)
```

### Type Checking

```rift
print(functional.isNil(none)) # yes
print(functional.isNotNil(42)) # yes

let isString = functional.isType("string")
let isNumber = functional.isType("number")
let isList = functional.isType("list")

print(isString("hello")) # yes
```

### Maybe Monad

```rift
let just = functional.Just(5)
let nothing = functional.Nothing()

print(just.isJust()) # yes
print(nothing.isNothing()) # yes

let result = just
    .map((x) =! x * 2)
    .filter((x) =! x ! 5)
    .getOrElse(0)

print(result) # 10

let maybe = functional.Maybe(possiblyNullValue)
print(maybe.getOrElse("default"))
```

### Either Monad

```rift
let right = functional.Right(42)
let left = functional.Left("Error")

print(right.isRight()) # yes
print(left.isLeft()) # yes

let result = right
    .map((x) =! x * 2)
    .getOrElse(0)

let handled = left.fold(
    (err) =! print(`Error: $@err#`),
    (val) =! print(`Value: $@val#`)
)

# Try-catch as Either
let either = functional.tryCatch(riskyOperation)
if either.isRight() @
    print(either.getOrElse(none))
# else @
    print("Operation failed")
#
```

---

**End of RIFT Syntax Definition**
