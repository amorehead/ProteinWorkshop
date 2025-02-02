Optimiser
================

These configs (generally) configure PyTorch ``Optimizer`` objects.

.. note::
    To use an alternative optimiser config, use a command like:

    .. code-block:: bash

        python src/train.py optimiser=<OPTIMISER_NAME> encoder=gvp dataset=cath task=inverse_folding

    where ``<OPTIMISER_NAME>`` is the name of the optimiser config.

.. note::
    To change the learning rate, use a command like:

    .. code-block:: bash

        python src/train.py optimizer.lr=0.0001 encoder=gvp dataset=cath task=inverse_folding

    where ``0.0001`` is the new learning rate.


ADAM (``adam``)
----------------------

.. code-block:: bash

    # Example usage:
    python src/train.py ... optimiser=adam optimiser.optimizer.lr=0.0001 ...

.. literalinclude:: ../../../../configs/optimiser/adam.yaml
   :language: yaml


ADAM-W (``adamw``)
----------------------

.. code-block:: bash

    # Example usage:
    python src/train.py ... optimiser=adamw optimiser.optimizer.lr=0.0001 ...


.. literalinclude:: ../../../../configs/optimiser/adamw.yaml
   :language: yaml


Lion (``lion``)
----------------------

.. code-block:: bash

    # Example usage:
    python src/train.py ... optimiser=lion optimiser.optimizer.lr=0.0001 ...

.. literalinclude:: ../../../../configs/optimiser/lion.yaml
   :language: yaml
