#!/bin/sh

[ -e "$HOME"/.profile ] && . "$HOME"/.profile

install_package() (
	pkgName="$1"
	echo "Try to install --${pkgName}--"
	case $(uname) in #()
		(Linux*)
			if which pacman >/dev/null 2>&1; then
				yes | pacman -S "$pkgName"
			elif which apt-get >/dev/null 2>&1; then
				DEBIAN_FRONTEND=noninteractive apt-get -y install "$pkgName"
			fi
			;; #()
		(Darwin*)
			yes | brew install "$pkgName"
			;; #()
		(*)
			;;
	esac
)


get_pkg_mgr() {
	case $(uname) in
		(Linux*)
			if  which pacman >/dev/null 2>&1; then
				echo 'pacman'
				return 0
			elif which apt-get >/dev/null 2>&1; then
				echo 'apt-get'
				return 0
			fi
			;;
		(Darwin*)
			echo 'homebrew'
			return 0
			;;
		(*)
			;;
	esac
	return 1
}

case $(uname) in
	(Linux*)
		if which apt-get >/dev/null 2>&1; then
			apt-get update
		fi
		;;
	(Darwin*)
		if ! brew --version 2>/dev/null; then
			#-f = -fail - fails quietly, i.e. no error page ...I think?
			#-s = -silent - don\'t show any sort of loading bar or such
			#-S = -show-error - idk
			#-L = -location - if page gets redirect, try again at new location
			/bin/bash -c "$(curl -fsSL \
				https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
		fi
		;;
	(*) ;;
esac

pkgMgrChoice=$(get_pkg_mgr)

[ -n "$pkgMgrChoice" ] || show_err_and_exit "No package manager set"

if ! git --version 2>/dev/null; then
	install_package git
fi

case $(uname) in
	(Linux*)
		if [ "$pkgMgrChoice" = 'apt-get' ]; then
			if ! dpkg -s autoconf 2>/dev/null; then
				install_package autoconf
			fi
			if ! dpkg -s patch 2>/dev/null; then
				install_package patch
			fi
			if ! dpkg -s build-essential 2>/dev/null; then
				install_package build-essential
			fi
			if ! dpkg -s rustc 2>/dev/null; then
				install_package rustc
			fi
			if ! dpkg -s libssl-dev 2>/dev/null; then
				install_package libssl-dev
			fi
			if ! dpkg -s libyaml-dev 2>/dev/null; then
				install_package libyaml-dev
			fi
			if ! dpkg -s libreadline6-dev 2>/dev/null; then
				install_package libreadline6-dev
			fi
			if ! dpkg -s zlib1g-dev 2>/dev/null; then
				install_package zlib1g-dev
			fi
			if ! dpkg -s libgmp-dev 2>/dev/null; then
				install_package libgmp-dev
			fi
			if ! dpkg -s libncurses5-dev 2>/dev/null; then
				install_package libncurses5-dev
			fi
			if ! dpkg -s libffi-dev 2>/dev/null; then
				install_package libffi-dev
			fi
			if ! dpkg -s libgdbm6 2>/dev/null; then
				install_package libgdbm6
			fi
			if ! dpkg -s libgdbm-dev 2>/dev/null; then
				install_package libgdbm-dev
			fi
			if ! dpkg -s libdb-dev 2>/dev/null; then
				install_package libdb-dev
			fi
			if ! dpkg -s uuid-dev 2>/dev/null; then
				install_package uuid-dev
			fi
		fi
		;;
	(*) ;;
esac

. "$HOME"/.profile &&

echo '##### asdf #####' &&
if ! asdf version >/dev/null; then
	git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.1
fi &&

echo '##### .profile edits #####' &&
if ! grep  -F 'export ASDF_DIR="$HOME/.asdf"' "$HOME"/.profile >/dev/null; then
	echo 'export ASDF_DIR="$HOME/.asdf"' >> "$HOME"/.profile
fi &&

if ! grep -F '. "$HOME/.asdf/asdf.sh"' "$HOME"/.profile >/dev/null; then
	echo '. "$HOME/.asdf/asdf.sh"' >> "$HOME"/.profile
fi &&

. "$HOME"/.profile &&

echo '##### asdf ruby plugin #####' &&
if ! asdf plugin list | grep 'ruby' >/dev/null; then
	asdf plugin add ruby https://github.com/asdf-vm/asdf-ruby.git
fi &&

echo '##### asdf install ruby #####' &&
if ! asdf list ruby 3.3.5 >/dev/null 2>&1; then
	asdf install ruby 3.3.5
fi &&

echo '##### asdf set local ruby version #####' &&
asdf <%= root ? "global" : "local" %> ruby 3.3.5


echo 'The end'