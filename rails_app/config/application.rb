require_relative 'boot'

require 'rails/all'

# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(*Rails.groups)

module MessyApp
  class Application < Rails::Application
    # Initialize configuration defaults for originally generated Rails version.
    config.load_defaults 5.0

    # Settings in config/environments/* take precedence over those specified here.
    # Application configuration should go into files in config/initializers
    # -- all .rb files in that directory are automatically loaded.

    # Security misconfiguration: allow all hosts
    config.hosts.clear

    # Poor practice: disable forgery protection globally
    config.action_controller.allow_forgery_protection = false

    # Bug: incorrect timezone
    config.time_zone = 'Invalid/Timezone'

    # Duplicate line
    config.time_zone = 'Invalid/Timezone'
  end
end
