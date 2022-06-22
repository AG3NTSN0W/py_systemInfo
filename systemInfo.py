import os
import psutil
import logging
import platform
from telegram import Update
from datetime import datetime
from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(filename='app.log',
        filemode='w',
        format='%(asctime)s | %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%m/%d/%Y %H:%M:%S'
    )
logger = logging.getLogger()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor  
    pass     

class Bot:
    def __init__(self, token, chatId):
        async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            logger.info('executing \'/info\' command') 
            if update.message.chat_id == chatId:
                await SystemInfo().get_cpu_info(update)
                await SystemInfo().get_memory_info(update)
                await SystemInfo().get_disk_info(update)
                await SystemInfo().get_temp_info(update)

        async def cpu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            logger.info('executing \'/cpu\' command') 
            if update.message.chat_id == chatId:
                await SystemInfo().get_cpu_info(update) 

        async def mem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            logger.info('executing \'/memory\' command') 
            if update.message.chat_id == chatId:
                await SystemInfo().get_memory_info(update)         

        async def disk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            logger.info('executing \'/disk\' command') 
            if update.message.chat_id == chatId:
                await SystemInfo().get_disk_info(update)  

        async def temp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            logger.info('executing \'/temperatur\' command') 
            if update.message.chat_id == chatId:
                await SystemInfo().get_temp_info(update)  

        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("info", info))
        app.add_handler(CommandHandler("memory", mem))
        app.add_handler(CommandHandler("cpu", cpu))
        app.add_handler(CommandHandler("disk", disk))
        app.add_handler(CommandHandler("temperatur", temp))

        app.run_polling()
    pass

class SystemInfo:

    separator = f'{"-"*30} \n'

    async def get_cpu_info(self, bot):
        cpufreq = psutil.cpu_freq()
        message = "<pre>"
        message += "CPU Usage Per Core: \n"
        message += self.separator
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            message += f'Core {i}: {percentage}% \n'
            logger.debug(f"Core {i}: {percentage}%")
        message += self.separator
        message += f"Total CPU Usage: {psutil.cpu_percent()}%"
        message += "</pre>" 
        logger.info(f"Sending CPU info to user")
        await bot.message.reply_text(text=message, parse_mode='HTML')
        

    async def get_memory_info(self, bot):
        # Memory Information
        message = "<pre>"
        message += "Memory Information \n"
        message += self.separator
        # get the memory details
        svmem = psutil.virtual_memory()
        message += f"Total: {get_size(svmem.total)} \n"
        message += f"Available: {get_size(svmem.available)} \n"
        message += f"Used: {get_size(svmem.used)} \n"
        message += f"Percentage: {svmem.percent}% \n"
        message += self.separator
        # get the swap memory details (if exists)
        message += "SWAP \n"
        message += self.separator
        swap = psutil.swap_memory()
        message += f"Total: {get_size(swap.total)} \n"
        message += f"Free: {get_size(swap.free)} \n"
        message += f"Used: {get_size(swap.used)} \n"
        message += f"Percentage: {swap.percent}% \n"
        message += "</pre>" 
        logger.info(f"Sending memory info to user")
        await bot.message.reply_text(text=message, parse_mode='HTML')
        pass

    async def get_disk_info(self, bot):
        message = "<pre>"
        message += "Partitions and Usage:\n"
        message += self.separator
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            message += f"Device: {partition.device}\n"
            message += f" Mountpoint: {partition.mountpoint}\n"
            message += f" File system type: {partition.fstype}\n"
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            message += f" Total Size: {get_size(partition_usage.total)}\n"
            message += f" Used: {get_size(partition_usage.used)}\n"
            message += f" Free: {get_size(partition_usage.free)}\n"
            message += f" Percentage: {partition_usage.percent}%\n"
            message += self.separator
        message += "</pre>" 
        logger.info(f"Sending disk info to user")
        await bot.message.reply_text(text=message, parse_mode='HTML')
        pass    

    async def get_temp_info(self, bot):
        message = "<pre>"
        message += "Temperatures: \n"
        message += self.separator
        temps = psutil.sensors_temperatures(fahrenheit=False)
        if not temps:
            await bot.message.reply_text(text="can't read any temperature", parse_mode='HTML')
            return

        for name, entries in temps.items():
            message += f"{name} \n"
            for entry in entries:
                message += f" {entry.label} : {entry.current}°C\n"
            message += self.separator

        message += "</pre>" 
        logger.info(f"Sending temperatures info to user")
        await bot.message.reply_text(text=message, parse_mode='HTML')
        pass      


if __name__ == "__main__":
    try: 
        botToken = os.environ['botToken']
        chatId = int(os.environ['chatId'])
        logger.info(f'App started') 
        logger.info(f'Bot Token: {botToken}') 
        logger.info(f'Chat Id: {chatId}')
        Bot(botToken, chatId)
    except KeyError as e:
        logger.error(f'Missing environment variable: {e}') 
    except Exception as e:     
        logger.error(f"{e}")         