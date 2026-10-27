// Affiliate links for the discount cards, used on every page.
// Replace these URLs with your own affiliate links when you have them.
var CARD_LINKS = {
  goodrx: "https://www.goodrx.com/",
  ndc: "https://www.nationaldrugcard.com/"
};
document.querySelectorAll("[data-card]").forEach(function (a) {
  var u = CARD_LINKS[a.getAttribute("data-card")];
  if (u) a.href = u;
});
