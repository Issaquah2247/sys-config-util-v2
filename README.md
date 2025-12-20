# Mira Bot - Wild West Discord Bot 🤠

**Run your own Wild West Discord bot locally on your PC!**

Howdy, partner! I'm Mira, your Wild West companion. Join a gang, rob banks, trade contraband, and build your fortune in the frontier!

## 🚀 One-Click Installation

### Prerequisites
- Windows PC
- Python 3.8 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))

### Installation Steps

1. **Clone or Download this repository**
   ```bash
   git clone https://github.com/Issaquah2247/sys-config-util-v2.git
   cd sys-config-util-v2
   ```

2. **Run the one-click installer**
   - Double-click `install.bat`
   - The script will:
     - Check for Python installation
     - Install all required dependencies
     - Set up your configuration
     - Ask for your Discord Bot Token

3. **Get Your Discord Bot Token**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application or select existing one
   - Go to "Bot" section
   - Click "Reset Token" and copy it
   - Paste it when the installer asks

4. **Run the bot**
   - Double-click `run.bat` or
   - Run `python main.py` in terminal

## 🎮 Features

- **Gang System**: Join the Daltons, Wild Bunch, Josie Gang, Law Officers, or Town Bankers
- **Economy**: Earn money through work, heists, and trading
- **Drug Trading**: Make and sell opium, whiskey, and tobacco
- **Heists**: Plan and execute bank robberies with your gang
- **Duels**: Challenge other players to gunfights
- **Roles**: Leader, Planner, Muscle, Robber, Horse Manager, Town Drunk, Weapons Master, Medic
- **Law Enforcement**: Officers can arrest outlaws

## 📋 Commands

The bot will display all available commands in the terminal when it starts. Here's a preview:

### Basic Commands
- `!mira` - Introduction to Mira
- `!help` - Complete command guide
- `!balance` or `!bal` - Check your cash and stats

### Gang Commands
- `!joinggang [gang]` - Join a gang (daltons, wildbunch, josie, officers, bankers)
- `!assignrole [@member] [role]` - Assign roles (Leader only)

### Economy Commands
- `!work` - Earn money from jobs
- `!makedrug [type] [amount]` - Craft drugs (opium, whiskey, tobacco)
- `!selldrug [type] [amount]` - Sell your drugs

### Action Commands
- `!heist` - Start a bank heist (requires gang)
- `!rob [@member]` - Attempt to rob another player
- `!duel [@member] [amount]` - Challenge to a duel
- `!arrest [@member]` - Arrest outlaws (Officers only)

## 🛠️ Technical Details

- **Language**: Python 3.x
- **Library**: discord.py
- **Database**: SQLite3 (local database)
- **Runs 24/7** on your PC as long as the terminal stays open

## 📝 Configuration

Your Discord token is stored in `.env` file:
```
DISCORD_TOKEN=your_token_here
```

## 🔧 Manual Installation (Advanced)

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo DISCORD_TOKEN=your_token_here > .env

# Run the bot
python main.py
```

## 📊 Terminal Display

When running, the terminal will show:
- Bot status (Online/Offline)
- All available commands
- Command descriptions
- Real-time activity logs
- Server connections

## 🤝 Support

Need help? Check out:
- Discord.py Documentation: https://discordpy.readthedocs.io/
- Discord Developer Portal: https://discord.com/developers/docs

## 📜 License

Free to use and modify for personal projects!

---

**Built with ❤️ by Issaquah2247**
