export default (value, currency) => {
  if (currency === 'USD') {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(value);
  }
  if (currency === 'RUB') {
    return new Intl.NumberFormat('ru-RU', { style: 'currency', currency }).format(value);
  }
  return value;
};
