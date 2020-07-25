require 'json'

class HighscoresController < ApplicationController
  def get_top_ten
    # run code to render the top 10 in json format
    highscores = Highscore.order('time asc').limit(10)    # gets the 10 users with lowest time
    highscorelist = Array.new                             # initialises new array
    highscores.each do |score|                            # iterating through each object in @highscores
      highscorelist.push({                                # appends a new hash object to the new array
        user: score.user,
        time: score.time
      }) 
    end
    jsonlist = highscorelist.to_json                      # convert to json format
    render json: jsonlist                                 # renders the json in the view
  end

  def create_new_highscore
    # posts the new highscore list
    if request.user_agent == 'The Tower - Game Client'
      highscore = Highscore.new(user: params[:user], 
                                time: params[:time])
      if highscore.save
        render status: 201                                # Highscore created
      else
        render status: 500                                # server issue if cannot post
      end
    else
      render status: 401                                  # Unauthorised
    end
  end
end
