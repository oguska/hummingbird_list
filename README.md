# hummingbird_list
   Creates a [flexget](http://flexget.com) entry for each item in your hummingbird.me list.
   
   Place `hummingbird_list.py` and/or `hummingbird_movies.py` in `./flexget/plugins/`

   ```
   hummingbird_list:
      username: <value> (required)
      lists:
      	- <currently-watching|plan-to-watch|completed|on-hold|dropped>
      	- <currently-watching|plan-to-watch|completed|on-hold|dropped>
      latest: <yes|no>
      currentonly: <yes|no>
      finishedonly: <yes|no>
   ```
     
   - Not specifying any lists will create entries for your whole library  
   - Enabling `latest` will emit entries for the latest episode you have watched, as opposed to emitting shows
   - Enabling `currentonly` will reject items that are not currently airing
   - Enabling `finishedonly` will reject items that are not finished airing
    
   ```
   hummingbird_movies:
      username: <value> (required)
      lists: 
      	- <currently-watching|plan-to-watch|completed|on-hold|dropped>
      	- <currently-watching|plan-to-watch|completed|on-hold|dropped>
   ```
