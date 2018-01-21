//Cree par Falafel
//Utilisable librement ,mais ne pas dire l'avoir cree


const Discord = require("discord.js");
const client = new Discord.Client();
const token = "VOTRETOKEN";
var prefix = "VOTRE PREFIX";
var mention = "VOTREMENTION"

client.on("ready", () => {
console.log('Allumage ou Reboot réussi !')
setInterval(function(){
client.user.setGame("PREMIERJEU")}, 15000); //Change le jeu toutes 15 secondes

setTimeout(function(){
setInterval(function(){
client.user.setGame("DEUXIÈME JEU")}, 15000)}, 15000)
});

//simple reponse
client.on('message', message => {
if(message.content === prefix + "reponse") {
message.reply('Ceci est une reponse !') 
}
});

//embeds
client.on('message', message => {
if(message.content === prefix + "aide") {
message.react('✅') 
	var embed = new Discord.RichEmbed()
  .setTitle('Titre')
		.setColor('#ff00ce')
		.addField('Ligne','ligne2')
   .addField('ligne','ligne2')
message.channel.send(embed)
}
});

//login
//ne pas toucher ni remplacer

client.login(token)