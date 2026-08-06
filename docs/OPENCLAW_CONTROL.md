# OpenClaw Control

## Master

OpenClaw on U50 controls the remote Fondazione node.

## Node

Remote VPS:

35.239.91.187

The node executes services but does not make autonomous decisions.

## Allowed operations

- deploy
- update
- start
- pause
- stop
- report
- health checks

## Restrictions

OpenClaw must not:

- bypass Risk Engine
- enable live trading automatically
- modify strategies without user approval
- store secrets in GitHub
