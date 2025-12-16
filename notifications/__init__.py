"""Notifications package initialization"""
from notifications.notifier_interface import INotifier
from notifications.notifiers import EmailNotifier, SMSNotifier, ConsoleNotifier, MultiNotifier