---
title: "Solidity view vs pure: Function Mutability, Variable Types, and Data Locations Explained"
excerpt: "What pure, view, payable, and nonpayable actually restrict a function from doing, plus storage, memory, and calldata — grounded in a real Foundry compiler error from a FundMe project."
category: "blockchain"
banner: "/images/banner-foundry-debug.svg"
metaLine: "Solidity Fundamentals"
pubDate: 2026-09-15
stack: ["Solidity", "Foundry"]
---

If you are learning Solidity, two keywords you will encounter very quickly are `view` and `pure`.

At first they seem simple:

```solidity
function getValue() public view returns (uint256) {
    return value;
}
```

and:

```solidity
function add(uint256 a, uint256 b)
    public
    pure
    returns (uint256)
{
    return a + b;
}
```

But the difference becomes much clearer when the Solidity compiler rejects your code.

I recently encountered exactly that while testing a FundMe contract with Foundry — see the [Foundry debugging series](/foundry) for the other real errors that came out of that same project. The compiler reported:

```text
Function declared as pure, but this expression
(potentially) reads from the environment or state
and thus requires "view".
```

It also reported:

```text
Function cannot be declared as pure because this
expression (potentially) modifies the state.
```

Understanding why these errors happen requires understanding three related Solidity concepts:

1. Function state mutability: `pure`, `view`, `payable`, and the default non-payable behavior.
2. Solidity variable and data types.
3. Data locations such as `storage`, `memory`, and `calldata`.

Let's examine them together.

---

## What Does Function Mutability Mean in Solidity?

Solidity functions can declare restrictions describing what they are allowed to do with blockchain state.

The four important cases are:

| Function type         | Read blockchain state? | Modify blockchain state? | Receive ETH? |
| --------------------- | ---------------------: | -----------------------: | -----------: |
| `pure`                |                     No |                       No |           No |
| `view`                |                    Yes |                       No |           No |
| Default / non-payable |                    Yes |                      Yes |           No |
| `payable`             |                    Yes |                      Yes |          Yes |

The [official Solidity documentation on contracts](https://docs.soliditylang.org/en/latest/contracts.html) defines `pure` as disallowing access to or modification of state, while `view` disallows modification but permits reading state. `payable` allows Ether to accompany a function call.

This gives us a useful mental model:

```text
pure
  ↓
view
  ↓
non-payable
```

As we move downward, the function is allowed to interact with more blockchain state.

`payable` is different because it specifically determines whether a function can receive Ether.

---

## Solidity `pure` Functions

A `pure` function does not depend on contract state or blockchain state.

Its output should depend only on information such as its parameters and locally calculated values.

For example:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.36;

contract Calculator {
    function add(
        uint256 a,
        uint256 b
    ) public pure returns (uint256) {
        return a + b;
    }
}
```

The function receives two values:

```solidity
a
b
```

and calculates:

```solidity
a + b
```

It does not need to read anything stored in the contract.

That makes `pure` appropriate.

Another example is:

```solidity
function calculateDouble(
    uint256 number
) public pure returns (uint256) {
    uint256 result = number * 2;

    return result;
}
```

Again, everything needed by the function comes from its argument or local variables.

---

### What Can't a `pure` Function Do?

Suppose we create a state variable:

```solidity
uint256 public favoriteNumber = 42;
```

Then try this:

```solidity
function getFavoriteNumber()
    public
    pure
    returns (uint256)
{
    return favoriteNumber;
}
```

This will not compile.

Why?

Because:

```solidity
favoriteNumber
```

is a **state variable**.

The function is reading information stored by the contract.

A `pure` function promises that it does not access contract state, so the compiler rejects the function.

The correct declaration is:

```solidity
function getFavoriteNumber()
    public
    view
    returns (uint256)
{
    return favoriteNumber;
}
```

The [official Solidity documentation](https://docs.soliditylang.org/en/latest/types.html) describes state variables as variables whose values are stored as part of contract state, normally in persistent contract storage.

---

## Solidity `view` Functions

A `view` function can **read blockchain or contract state but cannot modify it**.

Consider:

```solidity
contract Counter {
    uint256 public count = 10;

    function getCount()
        public
        view
        returns (uint256)
    {
        return count;
    }
}
```

The function reads:

```solidity
count
```

but never changes it.

Therefore:

```solidity
view
```

is appropriate.

You can think of `view` as saying:

> "I need to look at blockchain state, but I promise not to change it."

---

### A `view` Function Cannot Modify State

This code is incorrect:

```solidity
uint256 public count;

function increaseCount() public view {
    count++;
}
```

The problem is:

```solidity
count++;
```

changes contract storage.

The function therefore cannot be `view`.

The correct version is:

```solidity
function increaseCount() public {
    count++;
}
```

Notice that there is no `view`, `pure`, or `payable` keyword.

That is a normal state-changing function.

---

## The Default: Non-Payable Functions

A normal Solidity function might look like:

```solidity
function setNumber(uint256 newNumber) public {
    number = newNumber;
}
```

This function can read and modify state.

Because it is not declared `payable`, however, callers cannot normally attach Ether to the function call.

At the ABI level, Solidity identifies this state mutability as `nonpayable`. The [ABI specification](https://docs.soliditylang.org/en/latest/abi-spec.html) distinguishes `pure`, `view`, `nonpayable`, and `payable` function state mutability.

You normally don't write:

```solidity
nonpayable
```

in Solidity source code.

Instead:

```solidity
function setNumber(uint256 newNumber) public {
```

is non-payable by default.

---

## Solidity `payable` Functions

A `payable` function is specifically allowed to receive Ether.

For example:

```solidity
function fund() public payable {
}
```

Now someone can call the function while sending ETH.

Inside the function, you can inspect the amount sent using:

```solidity
msg.value
```

For example:

```solidity
function fund() public payable {
    require(
        msg.value >= 0.01 ether,
        "Send at least 0.01 ETH"
    );
}
```

This pattern is common in crowdfunding contracts, payment contracts, DeFi applications, and teaching projects such as FundMe — see [why I built a blockchain notary](/blog/why-i-built-a-blockchain-notary) for another example of a Solidity project built around similar defensive-engineering habits.

The important distinction is:

```text
view      → reads state
pure      → does not read state
payable   → can receive ETH
```

These concepts answer different questions.

---

## A Real Foundry Error: `pure` vs State Modification

This distinction became particularly clear while I was testing a FundMe project with Foundry. If you've hit other Foundry errors, the [full debugging series](/foundry) covers the `--mt` flag, `forge-std/Test.sol` import issues, PATH problems on macOS, and Anvil/MetaMask mismatches.

My `HelperConfig.s.sol` contained logic similar to:

```solidity
function getOrCreateAnvilEthConfig()
    public
    pure
    returns (NetworkConfig memory)
{
    if (activeNetworkConfig.priceFeed != address(0)) {
        return activeNetworkConfig;
    }

    vm.startBroadcast();

    MockV3Aggregator mockPriceFeed =
        new MockV3Aggregator(
            DECIMALS,
            INITIAL_PRICE
        );

    vm.stopBroadcast();

    return NetworkConfig({
        priceFeed: address(mockPriceFeed)
    });
}
```

Running:

```bash
forge test --fork-url $SEPOLIA_RPC_URL
```

caused Solidity to complain that the function had been declared `pure`.

There are actually multiple problems.

---

### Problem 1: Reading a State Variable

The function contains:

```solidity
activeNetworkConfig.priceFeed
```

`activeNetworkConfig` is contract state.

A `pure` function cannot read that state.

Even this would already make `pure` invalid:

```solidity
if (activeNetworkConfig.priceFeed != address(0)) {
    return activeNetworkConfig;
}
```

If reading state were the only thing the function did, changing the function to `view` might solve the problem.

But there is another issue.

---

### Problem 2: Deploying a Contract Changes State

The function also contains:

```solidity
new MockV3Aggregator(
    DECIMALS,
    INITIAL_PRICE
);
```

The `new` expression creates a contract.

That means the function is doing more than reading state.

It is performing a state-changing action.

Therefore, this would also be incorrect:

```solidity
function getOrCreateAnvilEthConfig()
    public
    view
    returns (NetworkConfig memory)
```

`view` is still too restrictive.

The correct approach is to remove the mutability modifier:

```solidity
function getOrCreateAnvilEthConfig()
    public
    returns (NetworkConfig memory)
{
```

Now the function is allowed to interact with state as required.

Foundry provides Forge, Anvil, Cast, Chisel, and Solidity cheatcodes for smart-contract development and testing; cheatcodes can control execution and state in testing and scripting environments.

---

## `pure` vs `view`: The Easiest Way to Remember It

Consider these four functions:

```solidity
uint256 public number = 10;

function add(
    uint256 a,
    uint256 b
) public pure returns (uint256) {
    return a + b;
}

function getNumber()
    public
    view
    returns (uint256)
{
    return number;
}

function setNumber(uint256 newNumber) public {
    number = newNumber;
}

function deposit() public payable {
}
```

Their responsibilities are different.

```solidity
add()
```

performs computation only.

```solidity
getNumber()
```

reads contract state.

```solidity
setNumber()
```

changes contract state.

```solidity
deposit()
```

can receive ETH.

That distinction is far more useful than simply memorizing definitions.

---

## Function Mutability vs Function Visibility

Another common source of confusion is mixing up **mutability** and **visibility**.

These are different concepts.

Consider:

```solidity
function getPrice()
    public
    view
    returns (uint256)
{
    // ...
}
```

Here:

```solidity
public
```

describes **who can call the function**.

Meanwhile:

```solidity
view
```

describes **what the function can do to blockchain state**.

Common visibility modifiers are:

```solidity
public
private
internal
external
```

Common state-mutability categories are:

```solidity
pure
view
payable
non-payable
```

So a function can be:

```solidity
external view
```

or:

```solidity
public pure
```

or:

```solidity
external payable
```

because visibility and mutability solve separate problems.

---

## Solidity Variable Types

Understanding `pure` and `view` also becomes easier once you understand how Solidity handles variables.

Solidity is a statically typed language, meaning the type of a variable must be known. The [official documentation on types](https://docs.soliditylang.org/en/latest/types.html) divides Solidity types into categories including value types, reference types, mappings, and user-defined types.

Let's look at the most important ones.

---

## Value Types in Solidity

Value types contain their values directly.

Common examples include:

```solidity
bool
uint256
int256
address
bytes32
```

For example:

```solidity
bool public isActive = true;

uint256 public balance = 100;

int256 public temperature = -5;

address public owner;
```

Solidity supports unsigned integers such as:

```solidity
uint8
uint16
uint32
uint64
uint128
uint256
```

and signed integers such as:

```solidity
int8
int16
int32
int64
int128
int256
```

`uint` is an alias for:

```solidity
uint256
```

and `int` is an alias for:

```solidity
int256
```

Value types are copied when passed or assigned rather than behaving like references to the same data.

---

## `address` and `address payable`

Ethereum addresses can be represented using:

```solidity
address
```

For example:

```solidity
address public owner;
```

An address intended for operations that involve receiving Ether may need:

```solidity
address payable
```

For example:

```solidity
address payable public recipient;
```

These two concepts should not be confused with a **payable function**.

```solidity
address payable
```

is an address type.

```solidity
function deposit() public payable
```

declares a function capable of receiving ETH.

They use the same word because both relate to Ether transfers, but they apply to different Solidity constructs.

---

## Reference Types in Solidity

Reference types do not always behave like simple copied values.

Important reference types include:

```solidity
arrays
structs
```

Mappings also have special reference/storage behavior.

For example:

```solidity
uint256[] public numbers;
```

A struct could look like:

```solidity
struct Person {
    string name;
    uint256 age;
}
```

and a mapping could look like:

```solidity
mapping(address => uint256) public balances;
```

According to the [Solidity documentation on reference types](https://docs.soliditylang.org/en/latest/types.html#reference-types), reference types require careful handling because multiple variables may refer to the same underlying data. Their data location determines where that data lives.

That leads to one of Solidity's most important concepts.

---

## `storage`, `memory`, and `calldata` in Solidity

Developers coming from JavaScript, Python, Java, or C++ often find Solidity's data-location keywords unusual.

The three locations you will see most often are:

```solidity
storage
memory
calldata
```

They describe **where reference-type data lives**. Solidity's [documentation on data location](https://docs.soliditylang.org/en/latest/types.html#data-location) defines these three primary data locations for reference types.

---

### `storage`

`storage` represents persistent contract storage.

Consider:

```solidity
string public name = "Ahmed";
```

Because this is a state variable, its value belongs to contract storage.

Storage persists between transactions.

For example:

```solidity
struct User {
    string name;
    uint256 age;
}

User public user;
```

The `user` state variable remains part of the contract state until something changes it.

Persistent storage is comparatively expensive, so developers should be deliberate about what they store on-chain. The Solidity documentation describes contract storage as persistent across function calls and transactions.

---

### `memory`

`memory` is temporary.

For example:

```solidity
function createMessage()
    public
    pure
    returns (string memory)
{
    string memory message = "Hello Solidity";

    return message;
}
```

The `message` variable only needs to exist while the function executes.

It does not become permanent contract state.

Another example:

```solidity
function processNumbers(
    uint256[] memory numbers
) public pure returns (uint256) {
    return numbers.length;
}
```

Once the function call is finished, that memory is not persistent contract storage.

---

### `calldata`

`calldata` is commonly used for function arguments that should not be modified.

For example:

```solidity
function processNames(
    string[] calldata names
) external pure returns (uint256) {
    return names.length;
}
```

The Solidity documentation describes calldata as non-modifiable and non-persistent and notes that using it can avoid unnecessary copies when appropriate.

A useful rule of thumb is:

```text
storage  → persistent blockchain state
memory   → temporary modifiable data
calldata → temporary read-only input data
```

---

## `storage` vs `memory`: Why the Difference Matters

Suppose we have:

```solidity
struct Person {
    string name;
    uint256 age;
}

Person public person;
```

Now consider:

```solidity
function updateAge(uint256 newAge) public {
    Person storage currentPerson = person;

    currentPerson.age = newAge;
}
```

Here:

```solidity
Person storage currentPerson
```

points to the actual state variable.

Changing:

```solidity
currentPerson.age
```

therefore changes:

```solidity
person.age
```

Now compare that concept with a memory copy.

Assignments that cross data locations can result in copies, while storage references can refer to the existing storage object. The exact assignment behavior is documented in the [data location and assignment behaviour](https://docs.soliditylang.org/en/latest/types.html#data-location-and-assignment-behaviour) section of the docs, because it affects both correctness and gas usage.

---

## State Variables, Local Variables, and Function Parameters

Where a variable is declared also matters.

A state variable exists at contract level:

```solidity
contract Example {
    uint256 public number;
}
```

A local variable exists inside a function:

```solidity
function calculate()
    public
    pure
    returns (uint256)
{
    uint256 result = 5 + 10;

    return result;
}
```

A function parameter receives information from the caller:

```solidity
function multiply(
    uint256 a,
    uint256 b
) public pure returns (uint256) {
    return a * b;
}
```

Here:

```solidity
number
```

is state.

```solidity
result
```

is local.

```solidity
a
b
```

are parameters.

This distinction directly affects whether `pure` or `view` is appropriate.

---

## `constant` Variables in Solidity

Sometimes a value will never change.

Solidity lets us declare such a state variable using:

```solidity
constant
```

For example:

```solidity
uint256 public constant MINIMUM_USD = 5e18;
```

The value must be known at compile time.

Another example:

```solidity
uint256 public constant MAX_USERS = 1000;
```

`constant` is useful for values that are permanently fixed.

The [official Solidity documentation on constant and immutable state variables](https://docs.soliditylang.org/en/latest/contracts.html#constant-and-immutable-state-variables) states that constant state variables must have values fixed at compile time.

---

## `immutable` Variables in Solidity

`immutable` is similar to `constant`, but its value can be assigned during contract construction.

For example:

```solidity
address public immutable OWNER;

constructor() {
    OWNER = msg.sender;
}
```

Different deployments may therefore have different owners.

But once the contract has been deployed, that immutable value cannot be changed.

This distinction makes:

```solidity
constant
```

appropriate when the value is known during compilation, while:

```solidity
immutable
```

is useful when the value becomes known during deployment.

The same section of the Solidity documentation linked above specifically distinguishes compile-time `constant` values from `immutable` values that may be assigned during construction.

---

## Putting Everything Together

Here is a small contract demonstrating several of these concepts:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.36;

contract SolidityTypesExample {
    uint256 public number = 10;

    uint256 public constant MAX_VALUE = 1000;

    address public immutable owner;

    mapping(address => uint256) public balances;

    constructor() {
        owner = msg.sender;
    }

    // PURE:
    // Uses only parameters and calculation.
    function add(
        uint256 a,
        uint256 b
    ) public pure returns (uint256) {
        return a + b;
    }

    // VIEW:
    // Reads contract state.
    function getNumber()
        public
        view
        returns (uint256)
    {
        return number;
    }

    // STATE-CHANGING:
    // Modifies storage.
    function setNumber(
        uint256 newNumber
    ) public {
        require(newNumber <= MAX_VALUE);

        number = newNumber;
    }

    // PAYABLE:
    // Can receive ETH.
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // VIEW:
    // Reads the contract's ETH balance.
    function getContractBalance()
        public
        view
        returns (uint256)
    {
        return address(this).balance;
    }

    // PURE + CALLDATA:
    // Reads external input but not contract state.
    function getArrayLength(
        uint256[] calldata values
    ) external pure returns (uint256) {
        return values.length;
    }
}
```

This example demonstrates that the keywords work together rather than independently.

The question is not simply:

> "Should this function be `view` or `pure`?"

A better debugging process is:

```text
Does the function modify blockchain state?
        │
        ├── Yes → normal state-changing function
        │
        └── No
             │
             ├── Does it read blockchain/contract state?
             │       │
             │       ├── Yes → view
             │       │
             │       └── No → pure
             │
             └── Does it need to receive ETH?
                     └── If yes, payable is required
```

That mental model makes compiler errors much easier to understand.

---

## Common Solidity Mutability Mistakes

One common mistake is declaring every getter `pure`.

If it reads a state variable:

```solidity
return price;
```

it normally needs to be `view`, not `pure`.

Another mistake is assuming `view` means "this function returns something."

It doesn't.

A function can return a value without being `view`:

```solidity
function increment()
    public
    returns (uint256)
{
    number++;

    return number;
}
```

The function returns a number but also modifies state.

Therefore it cannot be `view`.

Similarly, `pure` does not mean "simple function."

It specifically means the function does not access or modify blockchain state.

Finally, remember that `public`, `private`, `internal`, and `external` describe visibility, while `pure`, `view`, and `payable` describe state mutability.

---

## Frequently Asked Questions

### What is the difference between `view` and `pure` in Solidity?

A `view` function can read contract or blockchain state but cannot modify it. A `pure` function cannot read or modify blockchain state.

For example:

```solidity
uint256 public number = 10;

function getNumber()
    public
    view
    returns (uint256)
{
    return number;
}
```

uses `view` because it reads `number`.

Meanwhile:

```solidity
function double(
    uint256 x
) public pure returns (uint256) {
    return x * 2;
}
```

can be `pure` because the calculation depends only on its input.

---

### Can a `view` function change a state variable?

No.

This is invalid:

```solidity
function update() public view {
    number = 10;
}
```

Changing a state variable modifies contract state, which violates the `view` restriction.

---

### Can a `pure` function read a state variable?

No.

For example:

```solidity
function getNumber()
    public
    pure
    returns (uint256)
{
    return number;
}
```

will fail because `number` is contract state.

Use:

```solidity
view
```

instead.

---

### Can a `pure` function use function arguments?

Yes.

This is perfectly valid:

```solidity
function subtract(
    uint256 a,
    uint256 b
) public pure returns (uint256) {
    return a - b;
}
```

The values are provided directly to the function rather than being read from contract state.

---

### What happens if I don't specify `view`, `pure`, or `payable`?

The function is non-payable by default.

It can read and modify contract state, but Ether cannot normally be attached to the call. Solidity's ABI represents this category as `nonpayable`.

---

### What is the difference between `memory` and `calldata`?

Both are temporary rather than permanent contract storage.

`memory` data can be modified during execution, while `calldata` is non-modifiable input data.

When function arguments do not need to be modified, `calldata` can also avoid unnecessary copying.

---

### Is `storage` permanent?

Contract storage persists across function calls and transactions until contract logic changes the stored values. This is fundamentally different from memory, which is created for a call and does not become permanent state.

---

### Why does Foundry say "Function declared as pure"?

This is a Solidity compiler error rather than a problem with the `forge test` command itself.

It generally means the function was marked:

```solidity
pure
```

but its implementation reads blockchain state or performs an operation incompatible with a pure function.

Inspect the compiler's referenced line.

If the function only reads state, it may need:

```solidity
view
```

If it changes state, deploys a contract, or performs other state-changing operations, remove `pure` rather than blindly replacing it with `view`.

---

## Final Thoughts

`pure`, `view`, and `payable` are not simply decorations added to Solidity functions.

They describe important constraints on how a function interacts with the Ethereum execution environment.

The core distinction is straightforward:

```text
pure
→ computation without reading or modifying blockchain state

view
→ read blockchain state but don't modify it

normal/non-payable
→ read and modify state

payable
→ can receive Ether
```

At the same time:

```text
storage
→ persistent contract data

memory
→ temporary function data

calldata
→ temporary read-only input data
```

And for state variables:

```text
constant
→ fixed at compile time

immutable
→ assigned during construction and fixed afterward
```

Once these concepts are understood together, compiler errors such as:

```text
Function declared as pure, but this expression
potentially reads from the environment or state
```

stop looking mysterious.

Instead, the compiler is telling you something useful about what your function is actually doing.

In my FundMe example, the function wasn't really `pure` at all. It read the active network configuration, used Foundry scripting functionality, and deployed a mock price-feed contract.

Removing `pure` wasn't simply a way to silence the compiler.

It made the function declaration accurately describe the behavior of the code.

And that is exactly what Solidity's mutability system is designed to enforce.

If you're working through similar Foundry issues, the [debugging series](/foundry) covers five more real errors, or [get in touch](/contact) if you need help with a Solidity or Foundry project directly.

---

### References

This article was checked against the official Solidity documentation covering [contracts and state mutability](https://docs.soliditylang.org/en/latest/contracts.html), [types, value/reference types, and data locations](https://docs.soliditylang.org/en/latest/types.html), and the [contract ABI specification](https://docs.soliditylang.org/en/latest/abi-spec.html), as well as the official Foundry documentation for the development framework.
