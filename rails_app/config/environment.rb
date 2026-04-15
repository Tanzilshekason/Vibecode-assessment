# Load the Rails application.
require_relative 'application'

# Initialize the Rails application.
Rails.application.initialize!

# Poor practice: overriding Rails initialization
Rails.application.config.middleware.delete Rack::Sendfile
