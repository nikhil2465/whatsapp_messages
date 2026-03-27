"""
🏢 Enterprise WhatsApp Platform Manager
===================================
Perfect Enterprise Platform Management with Restore Functionality
"""

import os
import subprocess
import json
from datetime import datetime

class EnterprisePlatformManager:
    """Manager for Enterprise WhatsApp Communication Platform"""
    
    def __init__(self):
        self.platform_dir = os.getcwd()
        self.original_repo = "https://github.com/nikhil2465/whatsapp_messages"
        
        print("🏢 Enterprise WhatsApp Platform Manager")
        print("="*50)
        print(f"📍 Platform Directory: {self.platform_dir}")
        print(f"🌐 Original Repository: {self.original_repo}")
        print("="*50)
    
    def check_platform_status(self):
        """Check current platform status"""
        print("\n📊 Checking Platform Status...")
        
        try:
            # Check git status
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            print("📋 Git Status:")
            print(result.stdout)
            
            # Check current branch
            result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
            print(f"🌿 Current Branch: {result.stdout.strip()}")
            
            # Check remote
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            print(f"🌐 Remote Repository:")
            print(result.stdout)
            
            # Check if platform is clean
            if "working tree clean" in result.stdout:
                print("✅ Platform is clean - ready for development!")
            else:
                print("⚠️ Platform has uncommitted changes")
                
        except Exception as e:
            print(f"❌ Error checking status: {e}")
    
    def restore_original(self):
        """Restore clone to original state"""
        print("\n🔄 Restoring to Original State...")
        
        try:
            # Fetch latest from origin
            print("📥 Fetching latest from original...")
            subprocess.run(['git', 'fetch', 'origin'], check=True)
            
            # Reset to original
            print("🔄 Resetting to original state...")
            subprocess.run(['git', 'reset', '--hard', 'origin/master'], check=True)
            
            # Clean untracked files
            print("🧹 Cleaning untracked files...")
            subprocess.run(['git', 'clean', '-fd'], check=True)
            
            print("✅ Successfully restored to original state!")
            print("🎯 Your clone is now identical to the original!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during restore: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def sync_with_original(self):
        """Sync clone with latest original changes"""
        print("\n🔄 Syncing with Original...")
        
        try:
            # Pull latest changes
            print("📥 Pulling latest changes...")
            subprocess.run(['git', 'pull', 'origin', 'master'], check=True)
            
            print("✅ Successfully synced with original!")
            print("🎯 Your clone now has the latest updates!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during sync: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def save_to_original(self, message="Clone updates"):
        """Save clone changes to original repository"""
        print(f"\n💾 Saving Changes to Original...")
        
        try:
            # Add all changes
            print("📝 Adding changes...")
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Commit changes
            print("💾 Committing changes...")
            commit_message = f"{message} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Push to original
            print("📤 Pushing to original repository...")
            subprocess.run(['git', 'push', 'origin', 'master'], check=True)
            
            print("✅ Successfully saved to original repository!")
            print("🎯 Your changes are now available in the original!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during save: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def create_backup_point(self, name):
        """Create a backup point with tag"""
        print(f"\n📦 Creating Backup Point: {name}")
        
        try:
            # Create tag
            tag_name = f"backup-{name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            subprocess.run(['git', 'tag', tag_name], check=True)
            
            print(f"✅ Backup point created: {tag_name}")
            print("🎯 You can restore to this point anytime!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating backup: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def list_backup_points(self):
        """List all backup points"""
        print("\n📋 Available Backup Points:")
        
        try:
            result = subprocess.run(['git', 'tag'], capture_output=True, text=True)
            tags = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            if tags:
                for i, tag in enumerate(tags, 1):
                    if tag.startswith('backup-'):
                        print(f"{i}. 🏷️  {tag}")
            else:
                print("📭 No backup points found")
                
        except Exception as e:
            print(f"❌ Error listing backups: {e}")
    
    def restore_backup_point(self, tag_name):
        """Restore to specific backup point"""
        print(f"\n🔄 Restoring to Backup Point: {tag_name}")
        
        try:
            subprocess.run(['git', 'checkout', tag_name], check=True)
            print(f"✅ Successfully restored to {tag_name}")
            print("🎯 Your clone is now at the backup point!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error restoring backup: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    def show_menu(self):
        """Show platform management menu"""
        print("\n🏢 PLATFORM MANAGEMENT MENU:")
        print("="*50)
        print("1. 📊 Check Platform Status")
        print("2. 🔄 Restore to Original State")
        print("3. 📥 Sync with Original")
        print("4. 💾 Save Changes to Original")
        print("5. 📦 Create Backup Point")
        print("6. 📋 List Backup Points")
        print("7. 🔄 Restore Backup Point")
        print("8. ❌ Exit")
        print("="*50)
    
    def interactive_mode(self):
        """Interactive platform management"""
        while True:
            try:
                self.show_menu()
                choice = input("\n👉 Enter your choice (1-8): ").strip()
                
                if choice == "1":
                    self.check_platform_status()
                elif choice == "2":
                    confirm = input("⚠️ This will reset all changes. Continue? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.restore_original()
                elif choice == "3":
                    self.sync_with_original()
                elif choice == "4":
                    message = input("💾 Enter commit message: ").strip()
                    if message:
                        self.save_to_original(message)
                elif choice == "5":
                    name = input("📦 Enter backup name: ").strip()
                    if name:
                        self.create_backup_point(name)
                elif choice == "6":
                    self.list_backup_points()
                elif choice == "7":
                    self.list_backup_points()
                    tag = input("🔄 Enter backup tag to restore: ").strip()
                    if tag:
                        self.restore_backup_point(tag)
                elif choice == "8":
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-8")
                
                input("\n👉 Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("👉 Press Enter to continue...")

def main():
    """Main function"""
    manager = EnterprisePlatformManager()
    
    try:
        manager.interactive_mode()
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        print(f"❌ Main error: {e}")

if __name__ == "__main__":
    main()
