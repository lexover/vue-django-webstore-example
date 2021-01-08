export default (value) => {
  switch (value) {
    case 'NC':
      return 'Not confirmed';
    case 'CF':
      return 'Confirmed';
    case 'PD':
      return 'Paid';
    case 'SN':
      return 'Sent';
    case 'DL':
      return 'Delivered';
    default:
      return '';
  }
};
