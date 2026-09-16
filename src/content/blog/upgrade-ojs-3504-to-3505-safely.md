---
title: "How to Upgrade OJS 3.5.0-4 to OJS 3.5.0-5 Safely: Step-by-Step Guide"
excerpt: "A cautious, production-first upgrade path for the 3.5.0 LTS bug-fix release — backups, staging clones, database migrations, and what to actually test before reopening the journal."
category: "systems"
categoryLabel: "Systems & Infrastructure"
categoryColor: "#5B8CFF"
banner: "/images/banner-ojs.svg"
metaLine: "OJS Administration · Practical Guide"
pubDate: 2026-09-16
order: 11
stack: ["OJS", "PHP", "MySQL", "Sysadmin"]
---

If you are running Open Journal Systems (OJS) 3.5.0-4, upgrading to OJS 3.5.0-5 gives you the latest bug-fix release in the OJS 3.5.0 series — and, notably, the version PKP has designated for Long-Term Support.

PKP released OJS, OMP, and OPS 3.5.0-5 in July 2026. Unlike the intermediate 3.5.0-x maintenance releases before it, 3.5.0-5 carries an explicit LTS designation: PKP has committed to maintaining it with bug fixes and security patches for an extended period. If your journal has been waiting for a stable version to settle on, this is the one that argument points toward.

This guide explains a cautious way to upgrade an existing OJS 3.5.0-4 installation to OJS 3.5.0-5, with particular attention to production journal websites.

> **Important:** Never test an OJS upgrade for the first time on your live journal. Back up the database, uploaded files, configuration, plugins, and application files first. Ideally, clone the journal and perform the entire upgrade on the clone before upgrading production.

## OJS 3.5.0-4 vs 3.5.0-5

OJS 3.5.0-5 is not a completely new OJS generation. It is a bug-fix release in the existing 3.5.0 branch.

This makes an upgrade from:

```
OJS 3.5.0-4 → OJS 3.5.0-5
```

much smaller than a major upgrade such as:

```
OJS 3.3 → OJS 3.5
```

However, you should not treat the upgrade as simply replacing a few PHP files. OJS includes database upgrade migrations, so the official upgrade process still needs to be completed.

The full list of resolved issues for any given release is documented in PKP's release notes on GitHub. It's worth reviewing those notes as part of your upgrade planning rather than upgrading blind — particularly if you're tracking a specific bug that affected your installation.

## Before You Start: Back Up Everything

A reliable backup is the most important part of an OJS upgrade.

At minimum, back up these four components:

1. OJS database
2. OJS application directory
3. OJS `files_dir`
4. `config.inc.php`

You should also record which plugins and custom themes are installed.

### 1. Back Up the Database

If you use MySQL or MariaDB, you can create a database backup with `mysqldump`:

```bash
mysqldump -u root -p ojs_database > ojs_before_3505_upgrade.sql
```

Replace `ojs_database` with the actual name of your OJS database.

If you are using XAMPP on Windows, you can alternatively export the database through phpMyAdmin. Open phpMyAdmin, select the OJS database, choose **Export**, select the SQL format, and download the resulting `.sql` file.

Do not continue until you know that the database backup exists and can be restored if necessary. A backup you have never tested restoring is a hope, not a backup.

### 2. Back Up Your OJS Application

Make a complete copy of your existing OJS installation directory.

For example, if the installation is:

```
C:\xampp\htdocs\ojs
```

create a backup such as:

```
C:\backups\ojs-3.5.0-4
```

Do not rely only on the new OJS package as a rollback mechanism. Your existing installation may contain configuration changes, plugins, themes, public files, or other customizations that exist nowhere else.

### 3. Back Up the OJS Files Directory

Check `config.inc.php` for:

```
files_dir = ...
```

This directory contains files uploaded through OJS — submissions, galleys, supplementary files — and is therefore critical. Copy the entire directory to a safe backup location.

For security, `files_dir` should normally be located outside the publicly accessible web directory.

### 4. Save Your config.inc.php

Your existing `config.inc.php` contains important installation-specific settings, including database configuration, URL-related settings, email configuration, and the location of `files_dir`.

Save a separate copy before upgrading.

Do not simply replace your existing configuration with the new package's template configuration. Instead, compare your existing configuration with `config.TEMPLATE.inc.php` from the new OJS release and review whether the newer release introduces or changes configuration options.

OJS 3.5 introduced configuration changes involving areas such as application keys, encryption, scheduled tasks, queues, and caching, so configuration differences should not be ignored when maintaining a 3.5 installation.

### 5. Record Your Installed Plugins

Before upgrading, make a list of all installed third-party and custom plugins. Examples include:

- QuickSubmit
- Custom Header
- Custom Locale
- Shariff
- OAI/JATS-related plugins
- Crossref-related plugins
- ORCID integrations
- Custom themes

Plugin compatibility matters because a plugin that worked on an earlier OJS release may not necessarily work correctly after an upgrade.

This is not hypothetical. PKP's own issue tracker contains a task specifically for reviewing 3.5 plugins after a change to the structure of publication metadata, because that change had side effects for plugins already released for 3.5 — some of which could be broken as a result. Themes including Bootstrap3, Health Sciences, and Immersion all required follow-up fixes.

Do not assume that an old plugin version is compatible simply because OJS itself upgraded successfully.

### 6. Put the Journal Into Maintenance Mode

Before upgrading the production installation, prevent normal journal activity. You do not want editors, reviewers, or authors changing submissions while the database is being upgraded.

If possible, schedule the upgrade during a low-traffic period and tell journal staff about the maintenance window in advance.

## Performing the Upgrade

### 7. Download OJS 3.5.0-5

Download OJS 3.5.0-5 from an official PKP source. Avoid downloading modified OJS packages from random websites.

Extract the new OJS package into a separate directory rather than immediately overwriting the production installation — for example, `ojs-3.5.0-5`. This makes it easier to compare the old and new installations and reduces the chance of accidentally destroying your working installation.

### 8. Transfer Your Existing Configuration

Copy or carefully merge the required installation-specific configuration from the existing installation. Pay particular attention to `config.inc.php` and your existing `public/` content. You should also account for any custom themes, custom plugins, or deliberate code modifications.

Avoid blindly copying the entire old `plugins` directory over the new installation. Doing so can reintroduce old plugin code that is incompatible with the newer release.

### 9. Check File and Directory Permissions

Make sure the web server can access the directories OJS needs. Incorrect permissions can cause symptoms such as:

- Blank pages
- HTTP 500 errors
- Failed uploads
- Cache errors
- Plugin installation failures
- Failed scheduled tasks

If the journal worked before the upgrade, record the existing permissions before changing anything.

### 10. Run the OJS Upgrade

Once the new application files and configuration are ready, run the OJS database upgrade. From the OJS installation directory:

```bash
php tools/upgrade.php upgrade
```

On Windows/XAMPP, if `php` is not available globally in your PATH, you can invoke the XAMPP PHP executable directly:

```
C:\xampp\php\php.exe tools\upgrade.php upgrade
```

Run this command from the root directory of your new OJS installation. Wait for the process to finish.

Do not close the terminal or stop Apache/MySQL in the middle of a database migration.

The OJS upgrade definitions for the 3.5 branch contain migrations for application data and fixes, which is why replacing the PHP files alone is not sufficient.

### 11. Confirm That the Upgrade Completed

Do not assume success simply because the website loads.

First check the output produced by the upgrade command. The upgrade should finish successfully rather than terminating with a PHP exception, SQL error, or failed migration.

If an error occurs, save the complete error output before attempting random fixes. This information is extremely useful when diagnosing an OJS upgrade failure — and largely irreplaceable once you've started changing things.

### 12. Clear OJS Caches

After the upgrade, clear relevant OJS caches before investigating unusual interface behaviour. Depending on your installation and configuration, cached templates or application data from the previous version can produce confusing results.

Do not delete directories blindly. Verify what your installation is using and preserve backups.

## Testing Before You Reopen

### 13. Test the Journal Before Reopening It

This is one of the most frequently overlooked parts of an OJS upgrade. A homepage that loads successfully does not prove that the journal is fully functional.

**Public website tests.** Open several published articles and verify:

- Journal homepage
- Current issue
- Archives
- Article landing pages
- Abstracts
- PDF downloads
- Search
- Categories
- Announcements
- Navigation menus
- DOI links
- ORCID links
- Article statistics

**Editorial workflow tests.** Log in with appropriate test accounts and verify:

- Author submission
- Editor dashboard
- Submission assignment
- Reviewer invitation
- Reviewer response
- Review submission
- Editorial decisions
- Copyediting
- Production
- Publication scheduling

**Email tests.** Test important transactional emails, including:

- New account email
- Password reset
- Submission acknowledgement
- Reviewer invitation
- Editorial decision emails

Pay particular attention to email-template variables. An email being delivered successfully does not necessarily mean its template variables and links were rendered correctly.

**Plugin tests.** Open every important plugin and verify its settings and functionality. A successful core OJS upgrade does not guarantee that every plugin remains compatible.

### 14. Check PHP and Web Server Logs

If anything behaves unexpectedly, check your server logs. For XAMPP/Apache installations, the Apache and PHP error logs can often reveal problems that are not displayed in the browser.

Typical problems after an upgrade include `PHP Fatal error`, `Class not found`, `Undefined method`, `Permission denied`, or database-related errors.

Copy the complete error and timestamp before troubleshooting it.

### 15. Verify Scheduled Tasks

OJS 3.5 includes changes to scheduled-task and queue configuration. Check that scheduled tasks continue to run correctly after the upgrade, particularly if your journal depends on automated processes.

Review your new `config.TEMPLATE.inc.php` alongside your existing `config.inc.php` rather than assuming that configuration requirements have remained unchanged.

### 16. Verify DOI and Indexing Metadata

If your journal uses DOI registration or external indexing, inspect a few published articles after upgrading. Check:

- DOI metadata
- Article metadata
- Author names
- ORCID identifiers
- References
- Keywords
- Issue metadata
- OAI-PMH output

This is particularly important for journals that exchange metadata with services such as Crossref or external indexing systems. Running a current, supported version is part of what keeps your platform compatible with third-party integrations and indexing services.

### 17. Re-enable the Production Journal

Only reopen the journal after the major workflows have been tested. At minimum, verify:

```
Homepage → article → PDF
```

and:

```
Submission → review → editorial decision → production/publication
```

as well as email delivery and the journal's essential plugins.

Keep the pre-upgrade backup for some time instead of immediately deleting it.

## Recommended Upgrade Strategy for Production Journals

For an important journal, I recommend this workflow:

```
OJS 3.5.0-4 Production
        ↓
Create full backup
        ↓
Create test/staging clone
        ↓
Upgrade clone to 3.5.0-5
        ↓
Check database upgrade
        ↓
Test plugins
        ↓
Test submission workflow
        ↓
Test email
        ↓
Test PDFs and published articles
        ↓
Test DOI/OAI metadata
        ↓
Test statistics
        ↓
Upgrade production
        ↓
Final verification
```

This takes longer than directly upgrading the live server, but it gives you a much safer recovery path.

## What If the OJS Upgrade Fails?

Do not repeatedly rerun commands or manually edit database tables without first understanding the error.

Save:

- The exact upgrade command
- Complete error message
- PHP version
- Database version
- Current OJS version
- Target OJS version
- Relevant PHP/Apache logs

If you have a verified backup, you can restore the previous application files and database while investigating the problem. This is precisely why the database backup must be taken before running the upgrade command.

## Final Thoughts

Upgrading from OJS 3.5.0-4 to OJS 3.5.0-5 is a relatively small version change, but a production journal should still treat it as a real application and database migration.

The safest approach is simple:

```
Backup → Clone → Upgrade → Test → Production Upgrade → Verify
```

The LTS designation is the part worth weighing if you're deciding whether to do this now. PKP has committed to maintaining 3.5.0-5 with bug fixes and security patches for an extended period, which makes it a more defensible version to settle on than an intermediate maintenance release you'll need to move off again shortly.

More importantly: an upgrade is successful only when the entire journal workflow continues to work — not merely when the homepage loads.

---

## Frequently Asked Questions

**What is the latest OJS 3.5.0 bug-fix release?**

As of September 2026, OJS 3.5.0-5 is the released bug-fix version discussed in this guide, and it carries PKP's Long-Term Support designation. Work on subsequent 3.5.0-x releases is visible in PKP's public issue tracker but not yet released at the time of writing.

**Can I upgrade directly from OJS 3.5.0-4 to 3.5.0-5?**

Yes. Both releases belong to the OJS 3.5.0 series. You should still back up the installation and execute the OJS upgrade procedure because database migrations exist within the 3.5 branch.

**Do I need to back up my database before upgrading OJS?**

Yes. A database backup is essential because the OJS upgrade process can modify the database schema and data.

**What command upgrades the OJS database?**

From the OJS installation directory:

```bash
php tools/upgrade.php upgrade
```

If you use XAMPP on Windows and PHP is not in your PATH, you may need to call your XAMPP PHP executable directly.

**Should I overwrite my old OJS files with the new version?**

For a production installation, it is safer to prepare the new release separately and deliberately migrate your configuration, public content, compatible plugins, and customizations rather than blindly overwriting everything.

**How do I know whether an OJS upgrade succeeded?**

Do not judge success from the homepage alone. Confirm that the upgrade command completes successfully, then test submissions, editorial workflow, reviewer workflow, emails, PDFs, plugins, DOI/OAI metadata, statistics, and published content.

**Should I test an OJS upgrade locally first?**

Yes. For a production journal, upgrading a clone or staging installation first is much safer than making the live journal your first test.

---

*Last updated: September 2026*
