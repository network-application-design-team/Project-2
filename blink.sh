#!/bin/sh

# Common path for all GPIO access
BASE_GPIO_PATH=/sys/class/gpio

# Assign names to GPIO pin numbers for each light
RED=17
GREEN=27
BLUE=22

# Assign names to states
ON="1"
OFF="0"

# Utility function to export pin if not already exported
exportPin()
{
	if [ ! -e $BASE_GPIO_PATH/gpio$1 ]; then
		echo "$1" > $BASE_GPIO_PATH/export
	fi
}

# Utility function to set a pin as an output
setOutput()
{
	echo "out" > $BASE_GPIO_PATH/gpio$1/direction
}

# Utility function to change the state of a light
setLightState()
{
	echo $2 > $BASE_GPIO_PATH/gpio$1/value
}

# Utilityfunction to turn all lights off
allLightsOff()
{
	setLightState $RED $OFF
	setLightState $GREEN $OFF
	setLightState $BLUE $OFF
}

# ctrl-c handler for a clean shutdown
shutdown()
{
	allLightsOff
	exit 0
}

trap shutdown SIGINT

# Export pins so that we can use them
exportPin $RED
exportPin $GREEN
exportPin $BLUE

# Set pins as outputs
setOutput $RED
setOutput $GREEN
setOutput $BLUE

# Turn lights off to begin
allLightsOff

# Loop forever until Ctrl+C is hit
while :
do
	# Red
	setLightState $RED $ON
	sleep 3

	# Red and Green
	setLightState $GREEN $ON
	sleep 1

	#GREEN
	setLightState $RED $OFF

	# BLUE
	setLightState $BLUE $ON
	setLightState $GREEN $OFF
done
