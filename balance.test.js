const { expect } = require("@jest/globals");
const calculate_balance = require("./balance.js");

test("adding ammounts to positive value", () => {
  expect(calculate_balance([100, -200, 100, 200])).toBe("200.00");
});
test("adding ammounts to negative value", () => {
  expect(calculate_balance([100, -500, 100, -200])).toBe("-500.00");
});
