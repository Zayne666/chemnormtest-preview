(function () {
  const select = document.getElementById('siteLanguage');
  if (!select) return;
  const isChinese = location.pathname.includes('/zh/');
  select.value = isChinese ? 'zh' : 'en';
  select.addEventListener('change', () => {
    const file = location.pathname.split('/').pop() || 'index.html';
    const suffix = location.search + location.hash;
    if (select.value === 'zh' && !isChinese) location.href = 'zh/' + file + suffix;
    if (select.value === 'en' && isChinese) location.href = '../' + file + suffix;
  });
})();
