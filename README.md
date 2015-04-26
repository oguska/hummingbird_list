# hummingbird_list
Creates a [flexget](http://flexget.com) entry for each item in your hummingbird.me list.

   Syntax:
   ```
   hummingbird_list:
     username: <value>
     type: <shows|movies|all>
     list: <currently-watching|plan-to-watch|completed|on-hold|dropped|all>
     latest: <yes|no>
     currentonly: <yes|no>
   ```
     
   - Choosing shows will accept anything that's not a movie(TV, OVAs, ONAs, specials, etc.)
   - Enabling latest will emit entries for the latest episode you have watched, as opposed to emitting shows
   - Enabling currentonly will reject items that are shows(not movies) and also are not currently airing (I recommend keeping this enabled because I haven't tested it disabled)
   
   Here's my current setup:
   ```
   templates:
      transmit:
        transmission: yes
        clean_transmission:
          transmission_seed_limits: yes

   tasks:
     anime_config:
       priority: 1
       configure_series:
         settings:
           identified_by: sequence
         from:
           hummingbird_list:
             username: matthewdias
             type: all
             list: currently-watching
             latest: no
             currentonly: yes
       hummingbird_list:
         username: matthewdias
         type: all
         list: currently-watching
         latest: yes
         currentonly: yes
       accept_all: yes
       thetvdb_lookup: yes
       set_series_begin: yes
   
     anime_fetch:
       priority: 2
       configure_series:
         settings:
           quality: 720p
           identified_by: sequence
         from:
           hummingbird_list:
             username: matthewdias
             type: all
             list: currently-watching
             latest: no
             currentonly: yes
       content_filter:
         reject:
           - '*.rar'
           - '*.zip'
           - '*.avi'
       discover:
         what:
           - emit_series:
               from_start: yes
         from:
           - nyaa:
               category: anime eng
               filter: trusted only
       thetvdb_lookup: yes
       set:
         path: ~/Movies
         main_file_only: yes
         content_filename: "{{tvdb_series_name}} {{tvdb_episode}}"
         rename_like_files: yes
         skip_files:
           - '*.nfo'
           - '*.sfv'
           - '*[sS]ample*'
           - '*.txt'
       template: transmit
       pushbullet:
         apikey: <apikey>
         title: "Anime download started"
         body: "{{tvdb_series_name}} Episode {{tvdb_ep_id}}"
    ...
   ```
