from logging import basicConfig, info, INFO

basicConfig(
    level=INFO,
    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
)

__all__ = ['info']
