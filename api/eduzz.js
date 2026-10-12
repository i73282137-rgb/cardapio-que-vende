module.exports = async (req, res) => {
  if (req.method === 'GET') {
    res.writeHead(302, { Location: 'https://i73282137-rgb.github.io/cardapio-que-vende/' });
    return res.end();
  }
  if (req.method === 'POST') {
    return res.status(200).json({ ok: true, product: 'cardapio-que-vende' });
  }
  return res.status(405).json({ error: 'method_not_allowed' });
};
