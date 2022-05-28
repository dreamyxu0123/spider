var log = console.log.bind(console)
var len = document.querySelector('div.tx-text.info-txt.mb15').children.length
var arr = [...document.querySelector('div.tx-text.info-txt.mb15').children]
arr = arr.slice(1, len - 1)
var urls = []
for (const i of arr) {
  // log(i.children[0].src)
  urls.push(i.children[0].src)
}
log(urls)
