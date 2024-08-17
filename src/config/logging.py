from logging import basicConfig, info, INFO

basicConfig(
    level=INFO,
    format='%(levelname)s - %(asctime)s - %(filename)s - %(message)s'
)

__all__ = ['info']
