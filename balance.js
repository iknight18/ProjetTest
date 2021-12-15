function calculate_balance(amounts) {
  return amounts.reduce((acc, item) => (acc += item), 0).toFixed(2);
}
module.exports = calculate_balance;
