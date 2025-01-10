function init(){
        const args = process.argv.slice(2)
        const mineflayerViewer = require('prismarine-viewer').mineflayer
        const mineflayer = require('mineflayer') 
        const inventoryViewer = require('mineflayer-web-inventory')
        const bot = mineflayer.createBot({ host: '1.1.1.1', // minecraft server ip 
        username: args[0], // username to join as if auth is `offline`, else a unique identifier for this account. Switch if you want to change accounts 
        auth: 'offline', // for   offline mode servers, you can set this to 'offline'
        port: 25565, // set if you need a port that isn't 25565 
        version: "1.20.1"
        })
        bot.on('resourcePack',(url,hash) =>{
                bot.acceptResourcePack();
        });
        bot.once('spawn',()=>{
                mineflayerViewer(bot,{port:40001, firstPerson:true});
                mineflayerViewer(bot,{port:40002, firstPerson:false});
        })
        bot.on('death',()=>{
                bot.respawn()
        })
        bot.on('end',init)
}
init();
