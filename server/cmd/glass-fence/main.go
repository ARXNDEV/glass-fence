package main

import (
	"fmt"

	"github.com/rs/zerolog/log"

	glass-fence "github.com/arxndev/glass-fence/server"
	"github.com/arxndev/glass-fence/server/cmd"
	"github.com/arxndev/glass-fence/server/pkg/utils"
)

func main() {
	fmt.Print(utils.Colorf(glass-fence.Header, "server", glass-fence.Version))
	if err := cmd.Execute(); err != nil {
		log.Panic().Err(err).Msg("failed to execute command")
	}
}
