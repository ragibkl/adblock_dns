const fs = require('fs')
const Router = require('@koa/router')
const pify = require('pify')

const readFileAsync = pify(fs.readFile)
const router = new Router()

function filter (ip, data) {
  return data
    .split('\n')
    .filter(v => v.includes(`${ip}#`))
    .join('\n')
}

router.get('/', async ctx => {
  const { ip } = ctx.request
  const data = await readFileAsync('/logs/rpz_log.txt', 'utf8')
  const filteredData = filter(ip, data)
  ctx.body = `ip = ${ip}\n\n${filteredData}`
})

module.exports = router