import scrapy
import csv

class MatchesSpider(scrapy.Spider):
    
    name = "matches"
    date=input("donner une date : ")
   
    def start_requests(self):
         
         yield scrapy.Request(f'https://www.yallakora.com/match-center?date={self.date}')
    

    def parse(self, response):
        championShips = response.css("div.matchCard")
        match_details = []
        for championShip in championShips:
            championShip_title = championShip.css("h2::text").get().strip()
            all_matches = championShip.css("li")
            
            for match in all_matches:
                
                team_a = match.css("div.teamA p::text").get().strip()
                team_b = match.css("div.teamB p::text").get().strip()
                score=match.css("div.MResult span.score::text")[0].get().strip() + " -- "+match.css("div.MResult span.score::text")[1].get().strip()
                match_time = match.css("div.MResult span.time::text").get().strip()
                match_status = response.css("div.topData div.matchStatus span::text").get().strip()
                match_rank=match.css("div.topData div.date::text").get().strip()
                match_details.append({
                    "البطولة": championShip_title,
                    "المناسبة":match_rank,
                    "الفريق 1": team_a,
                     "الفريق 2": team_b,
                    "التوقيت": match_time,
                    " نتيجة المباراة": score,
                    " حالة المبارة": match_status
                })

        keys=match_details[0].keys()
        with open("Calendrier.csv",'w',encoding="utf-8-sig") as output_file:
            dict_writer=csv.DictWriter(output_file,keys)
            dict_writer.writeheader()
            dict_writer.writerows(match_details)
            print("file created")
        yield {'match_details': match_details}
        



