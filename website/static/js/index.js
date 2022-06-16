const puppeteer = require('puppeteer');
const { Client } = require("pg");

const client = new Client({
    user: "postgres",
    host: "localhost",
    database: "scrapy",
    password: "groupe5",
    port: "5432"
  });



const url = "https://www.materiel.net/recherche/iphone/";

(async () => { 
       
    const browser = await puppeteer.launch({headless: false})
    const page =  await browser.newPage()
    await  page.goto(url)
    const data = await page.evaluate(()=>{
        let data = []
        let elements = document.querySelectorAll('.c-products-list__item');
        for(let element of elements){
            data.push({
                titre: element.querySelector('.c-product__title').textContent,
                prix: element.querySelector('.o-product__price').textContent
            })  

        }
        return data;
    })
  
    console.log(data)
   client.connect()
   .then(() => console.log('connection successfully'))
   .then(()=>{
    for(let i of data){
    client.query("insert into olx(titre, prix) values($1, $2)", [i.titre, i.prix])
       }
   } )
//    .then(()=> client.query("select * from olx"))
//    .then(results => console.table(results.rows))
   .catch(e => console.log(e))
   .finally(() => client.end())

   await browser.close();
})();



