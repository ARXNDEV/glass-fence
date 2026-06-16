package main

import (
	"fmt"

	"github.com/rs/zerolog/log"

	neko "github.com/ARXNDEV/glass-fence/server"
	"github.com/ARXNDEV/glass-fence/server/cmd"
	"github.com/ARXNDEV/glass-fence/server/pkg/utils"
)

func main() {
	fmt.Print(utils.Colorf(neko.Header, "server", neko.Version))
	if err := cmd.Execute(); err != nil {
		log.Panic().Err(err).Msg("failed to execute command")
	}
}
