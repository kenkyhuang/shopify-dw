require 'shopify_api'
require 'json'
require_relative 'settings'

# API URL
ShopifyAPI::Base.site = "https://#{APIKEY}:#{PASSWORD}@#{SHOPNAME}.myshopify.com/admin"

# Shopify resources to pull
resources = [ShopifyAPI::Order, ShopifyAPI::Product]

# Minimum date 
updated_at_min = ARGV[0]

# Minimum # of seconds between API calls
CYCLE = 5

resources.each do |resource|
  
  record_count = resource.count({:updated_at_min => updated_at_min})

  # record_count = resource.find(:all, :params=>{:limit => 250, :updated_at_min => updated_at_min }).count
  # record_count = resource.count

  nb_pages = (record_count / 250.0).ceil
  puts "There are #{record_count} record(s)."
  puts "There are #{nb_pages} page(s)."

  start_time = Time.now
  1.upto(nb_pages) do |page|
    unless page == 1

      # Calculate time it took API call to run
      stop_time = Time.now
      puts "Last batch processing started at #{start_time.strftime('%I:%M%p')}"
      puts "The time is now #{stop_time.strftime('%I:%M%p')}"
      processing_duration = stop_time - start_time
      puts "The processing lasted #{processing_duration.to_i} seconds."

      # Wait minimum seconds between API calls
      wait_time = (CYCLE - processing_duration).ceil
      puts "We have to wait #{wait_time} seconds then we will resume."
      sleep wait_time

      # Reinitialize start time for next API call
      start_time = Time.now

    end

    # Make API calls
    puts "Doing page #{page}/#{nb_pages}..."
    records = resource.find( :all, :params => { :limit => 250, :page => page, :updated_at_min => updated_at_min } )
    
    # Write results to file
    File.open("json/#{resource}.json","a") do |f|
      records.each do |record|
        json = record.to_json
        f.puts(json)
      end
    end
  end
end


