require "fileutils"
require "salad_prep"

module Provincial
	using SaladPrep::StringEx

	Resorcerer = SaladPrep::Resorcerer
	Canary = SaladPrep::Canary
	BoxBox = SaladPrep::BoxBox
	Toob = SaladPrep::Toob

	PackageManagers = SaladPrep::Enums::PackageManagers
	SetupLvls = SaladPrep::Enums::SetupLvls

	class WSPNEgg < SaladPrep::Egg
		def app_lvl_definitions_script_path
			__FILE__
		end
	end

	class WSPNInstallion < SaladPrep::Installion

		def install_dependencies
			self.class.curl
			self.class.openssl
			self.class.ca_certificates
			self.class.nginx_and_setup(@egg, @w_spoon)
		end

	end

	Resorcerer.class_eval do
		def self.nginx_template
			conf = <<~CONF
				server {
					listen [::]:80;
					server_name <SERVER_NAME>;

					return 301 https://$host$request_uri;
				}

				server {
					listen <listen>;
					#should be the public key
					ssl_certificate <ssl_public_key>;
					#should be the private key
					ssl_certificate_key <ssl_private_key>;
					#should be the intermediate key if relevant
					#ssl_trusted_certificate <ssl_intermediate>;

					location / {
						root <CLIENT_DEST>;
						try_files $uri /index.html =404;

						location /what-is-robot-reading {
							try_files /what_is_robot_reading/index.html =404;
						}
					}


					server_name <SERVER_NAME>;
				}
			CONF
		end
	end

	@egg = WSPNEgg.new(
		project_name_0: "washpenny",
		local_repo_path: ENV["WSPN_LOCAL_REPO_DIR"],
		repo_url: ENV["WSPN_REPO_URL"],
		env_prefix: "WSPN",
		url_base: "washpenny",
		tld: "com",
		db_owner_name: "blank"
	)

	@browser_trust_introducer = SaladPrep::FirefoxTrustIntroducer.new
	@cert_retriever = SaladPrep::PorkbunCertRetriever.new(@egg)
	@spoon_handle = SaladPrep::WSpoon.spoon_handle(@egg)
	@where_spoon = nil
	@local_spoon = SaladPrep::LocalSpoon.new(
		@egg,
		@browser_trust_introducer,
		@spoon_handle
	)
	@remote_spoon = SaladPrep::RemoteSpoon.new(
		@egg,
		@spoon_handle,
		@cert_retriever
	)

	@where_spoon = @egg.is_local? ? @local_spoon : @remote_spoon

	@spoon_phone = SaladPrep::NginxPhone.new(
		@egg,
		SaladPrep::Resorcerer,
		@where_spoon
	)

	@w_spoon = SaladPrep::WSpoon.new(@egg, @where_spoon, @spoon_phone)
	@box_box = SaladPrep::BoxBox.new(@egg)
	@dbass = SaladPrep::NoopAss.new(@egg)
	@remote = SaladPrep::Remote.new(@egg)
	@client_launcher = SaladPrep::ClientLauncher.new(
		@egg
	)
	@api_launcher = SaladPrep::StaticAPILauncher.new(
		egg: @egg,
		dbass: @dbass,
		w_spoon: @w_spoon,
		client_launcher: @client_launcher
	)


	@installer = WSPNInstallion.new(
		egg: @egg
	)

	@binstallion = SaladPrep::Binstallion.new(
		@egg,
		File.join(
			@egg.repo_path,
			"dev_ops"
		)
	)

	def self.egg
		@egg
	end

	def self.box_box
		@box_box
	end

	def self.w_spoon
		@w_spoon
	end

	def self.remote
		@remote
	end

	def self.api_launcher
		@api_launcher
	end

	def self.client_launcher
		@client_launcher
	end

	def self.installion
		@installer
	end

	def self.binstallion
		@binstallion
	end

	def self.w_spoon
		@w_spoon
	end

	def self.test_honcho
		nil
	end



end